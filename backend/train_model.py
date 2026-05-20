import cv2
import os
import numpy as np

dataset_path = "dataset/gagana"

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

label_map = {"gagana": 0}

for img_name in os.listdir(dataset_path):
    img_path = os.path.join(dataset_path, img_name)
    img = cv2.imread(img_path, 0)

    faces.append(img)
    labels.append(0)

faces = np.array(faces)
labels = np.array(labels)

recognizer.train(faces, labels)

recognizer.save("trainer.yml")

print("Training completed")