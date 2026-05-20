import cv2
import numpy as np
import csv
from datetime import datetime
import os

# -----------------------------
# Load trained model
# -----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# -----------------------------
# Face detector
# -----------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# -----------------------------
# Label mapping (IMPORTANT: update names here)
# -----------------------------
names = {
    0: "Gagana",
    1: "John",
    2: "Alice"
}

# -----------------------------
# Attendance function
# -----------------------------
def mark_attendance(name):
    file_path = "attendance.csv"

    # create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("name,date,time\n")

    with open(file_path, "r+") as f:
        data = f.readlines()
        recorded_names = []

        for line in data:
            entry = line.split(",")
            if entry[0] != "name":
                recorded_names.append(entry[0])

        if name not in recorded_names:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            f.writelines(f"{name},{date},{time}\n")

# -----------------------------
# Camera
# -----------------------------
cap = cv2.VideoCapture(0)

print("Camera started... Press Q to exit")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        try:
            label, confidence = recognizer.predict(roi)

            if confidence < 80:
                name = names.get(label, "Unknown")
            else:
                name = "Unknown"

            mark_attendance(name)

            cv2.putText(frame, f"{name}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        except:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Face Recognition Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()