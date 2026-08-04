import cv2
import serial
import time
import hashlib
import os

from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# =========================
# SERIAL CONNECTION
# =========================

ser = serial.Serial('COM3', 115200)

time.sleep(2)

# =========================
# VARIABLES
# =========================

recording = False
cap = None
out = None
filename = ""

# Time when object was last detected
last_detected_time = time.time()

# Delay before stopping recording
STOP_DELAY = 3

# =========================
# AES KEY GENERATION
# =========================

key = get_random_bytes(16)

with open("secret.key", "wb") as f:
    f.write(key)

print("AES Secret Key Generated")

# =========================
# ENCRYPTION FUNCTION
# =========================

def encrypt_file(filename):

    cipher = AES.new(key, AES.MODE_EAX)

    with open(filename, 'rb') as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)

    encrypted_filename = filename + ".enc"

    with open(encrypted_filename, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    print("Encryption completed")

    return encrypted_filename

# =========================
# HASH FUNCTION
# =========================

def generate_hash(filename):

    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:

        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

# =========================
# START RECORDING FUNCTION
# =========================

def start_recording():

    global cap, out, filename, recording

    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    timestamp_name = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"evidence_{timestamp_name}.avi"

    out = cv2.VideoWriter(
        filename,
        fourcc,
        20.0,
        (640, 480)
    )

    recording = True

    print("Recording Started")

# =========================
# STOP RECORDING FUNCTION
# =========================

def stop_recording():

    global recording

    recording = False

    if cap:
        cap.release()

    if out:
        out.release()

    cv2.destroyAllWindows()

    print("Recording Stopped")

    # =========================
    # ENCRYPT VIDEO
    # =========================

    encrypted_file = encrypt_file(filename)

    # =========================
    # GENERATE HASH
    # =========================

    hash_value = generate_hash(encrypted_file)

    print("SHA-256 Hash:")
    print(hash_value)

    # =========================
    # SAVE LOG
    # =========================

    timestamp = datetime.now()

    with open("evidence_log.txt", "a") as log:

        log.write(f"""
Timestamp : {timestamp}
Original File : {filename}
Encrypted File : {encrypted_file}
SHA-256 : {hash_value}

==================================

""")

    print("Evidence Log Saved")

    # =========================
    # DELETE ORIGINAL FILE
    # =========================

    if os.path.exists(filename):

        os.remove(filename)

        print("Original File Deleted")

# =========================
# MAIN LOOP
# =========================

print("System Started")

while True:

    try:

        # =========================
        # READ SERIAL DATA
        # =========================

        if ser.in_waiting:

            data = ser.readline().decode().strip()

            print("Sensor:", data)

            # =========================
            # OBJECT DETECTED
            # =========================

            if "DETECTED" in data:

                last_detected_time = time.time()

                # Start recording only once
                if not recording:

                    print("Object Detected")

                    start_recording()

            # =========================
            # NO OBJECT DETECTED
            # =========================

            elif "NO_OBJECT" in data:

                # Stop only after delay
                if recording and (time.time() - last_detected_time > STOP_DELAY):

                    print("No Object Detected")

                    stop_recording()

        # =========================
        # RECORD VIDEO
        # =========================

        if recording and cap is not None:

            ret, frame = cap.read()

            if ret:

                out.write(frame)

                cv2.imshow("Secure Evidence Recording", frame)

        # =========================
        # PRESS Q TO EXIT
        # =========================

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:

        print("Error:", e)

        break

# =========================
# CLEANUP
# =========================

if cap:
    cap.release()

if out:
    out.release()

cv2.destroyAllWindows()

ser.close()

print("System Closed")