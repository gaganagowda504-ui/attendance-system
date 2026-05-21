from flask import Flask, request
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)
@app.route('/')
def home():
    return "Backend Running Successfully"
@app.route('/upload', methods=['POST'])
def upload():

    data = request.json

    name = data['name']

    image_data = data['image'].split(",")[1]

    img_bytes = base64.b64decode(image_data)

    np_arr = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        1.1,
        4
    )

    if len(faces) > 0:

        return {
            "message": f"{name} Attendance Marked"
        }

    else:

        return {
            "message": "No Face Detected"
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)