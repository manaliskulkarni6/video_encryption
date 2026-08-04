import cv2
import serial
import time

# Change COM port if needed
ser = serial.Serial('COM3', 115200)

recording = False
cap = None
out = None

while True:

    # Read serial data
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        print(data)

        # START RECORDING
        if "DETECTED" in data and not recording:

            print("Object detected - Starting recording...")

            cap = cv2.VideoCapture(0)

            # Video format
            fourcc = cv2.VideoWriter_fourcc(*'XVID')

            # Save video
            filename = f"output_{int(time.time())}.avi"

            out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

            recording = True

        # STOP RECORDING
        elif "NO_OBJECT" in data and recording:

            print("No object - Stopping recording...")

            recording = False

            if cap:
                cap.release()
                cap = None

            if out:
                out.release()
                out = None

            cv2.destroyAllWindows()

    # RECORD VIDEO
    if recording and cap is not None:

        ret, frame = cap.read()

        if ret:
            out.write(frame)

            cv2.imshow("Recording", frame)

        # Manual stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
if cap:
    cap.release()

if out:
    out.release()

cv2.destroyAllWindows()
ser.close()