import cv2
import classification
import os
import connection
import serial
import signal
import sys

# === Arduino Serial Setup ===
SerialObj = serial.Serial('COM18')
SerialObj.baudrate = 9600
SerialObj.bytesize = 8
SerialObj.parity   = 'N'
SerialObj.stopbits = 1
SerialObj.timeout  = None

# === Initialize Camera Once ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video device.")
    sys.exit()
print("Camera ready...")

# === Safe Exit Handler ===
def exit_handler(sig, frame):
    print("\nExiting safely...")
    cap.release()
    SerialObj.close()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

# === Snapshot & Classification ===
def classify_snapshot(frame):
    """Capture snapshot, run classification, then delete image."""
    snapshot_path = "snapshot.png"
    cv2.imwrite(snapshot_path, frame)
    print("Snapshot saved...")

    category = classification.infer(snapshot_path)
    generalisation = classification.generalisation(category)
    print(f"Classified: {category} ({generalisation})")

    os.remove(snapshot_path)
    return category, generalisation

# === Main Loop ===
print("Waiting for Arduino signal (b'C\\r\\n')...")

while True:
    ReceivedString = SerialObj.readline().strip()
    print("Received:", ReceivedString)

    if ReceivedString == b'C':
        ret, frame = cap.read()
        if not ret:
            print("Frame capture failed.")
            continue

        rcat, rgen = classify_snapshot(frame)

        # Send classification result back to Arduino
        SerialObj.write(rgen) 
