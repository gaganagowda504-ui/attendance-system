import cv2
import csv
import os
from datetime import datetime

# Load OpenCV models
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

names = {0: "Gagana"}

# Create attendance file if not exists
file = "attendance.csv"

if not os.path.exists(file):
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])

def mark_attendance(name):
    with open(file, "r+") as f:
        data = f.readlines()
        recorded_names = []

        for line in data:
            entry = line.split(",")
            recorded_names.append(entry[0])

        if name not in recorded_names:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            writer = csv.writer(f)
            writer.writerow([name, date, time])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(roi)

        if confidence < 80:
            name = names[label]
            mark_attendance(name)
        else:
            name = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()