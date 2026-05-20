import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

path = "faces"

faces = []
labels = []
label_map = {}
current_id = 0

for image_name in os.listdir(path):
    if image_name.endswith(".jpg") or image_name.endswith(".png"):

        label = image_name.split(".")[0]

        if label not in label_map:
            label_map[label] = current_id
            current_id += 1

        img_path = os.path.join(path, image_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        face = detector.detectMultiScale(img)

        for (x, y, w, h) in face:
            faces.append(img[y:y+h, x:x+w])
            labels.append(label_map[label])

recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

print("Training completed. trainer.yml created!")
print("Labels:", label_map)