import cv2
import numpy as np
import csv
from datetime import datetime

# Load model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Haar cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Labels
names = {0: "Gagana"}

# Attendance function
def mark_attendance(name):
    with open("attendance.csv", "r+") as f:
        data = f.readlines()
        recorded = []

        for line in data:
            entry = line.split(",")
            recorded.append(entry[0])

        if name not in recorded:
            now = datetime.now()
            dt = now.strftime("%Y-%m-%d,%H:%M:%S")
            f.writelines(f"\n{name},{dt}")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(roi)

        if confidence < 80:
            name = names.get(label, "Unknown")
        else:
            name = "Unknown"

        mark_attendance(name)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 