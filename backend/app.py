from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

CORS(app, origins="*")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

@app.route("/")
def home():
    return "Backend Running Successfully"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()

        name = data.get("name")
        image_data = data.get("image").split(",")[1]

        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            return jsonify({"message": f"{name} Attendance Marked"})
        else:
            return jsonify({"message": "No Face Detected"})

    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)