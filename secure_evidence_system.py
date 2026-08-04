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

# =========================
# VARIABLES
# =========================

recording = False
cap = None
out = None
filename = ""

# =========================
# AES KEY GENERATION
# =========================

key = get_random_bytes(16)

with open("secret.key", "wb") as f:
    f.write(key)

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
# MAIN LOOP
# =========================

while True:

    if ser.in_waiting:

        data = ser.readline().decode().strip()

        print(data)

        # =========================
        # START RECORDING
        # =========================

        if "DETECTED" in data and not recording:

            print("Object detected")

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

            print("Recording started")

        # =========================
        # STOP RECORDING
        # =========================

        elif "NO_OBJECT" in data and recording:

            print("No object detected")

            recording = False

            if cap:
                cap.release()

            if out:
                out.release()

            cv2.destroyAllWindows()

            print("Recording stopped")

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

            print("Evidence log saved")

            # Optional
            # Delete original file

            os.remove(filename)

            print("Original file deleted")

    # =========================
    # RECORD VIDEO
    # =========================

    if recording and cap is not None:

        ret, frame = cap.read()

        if ret:

            out.write(frame)

            cv2.imshow("Secure Recording", frame)

        # Press q to quit

        if cv2.waitKey(1) & 0xFF == ord('q'):
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
