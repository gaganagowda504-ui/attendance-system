from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Running Successfully"

@app.route("/attendance")
def attendance():
    data = []

    try:
        with open("attendance.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 3:
                    data.append({
                        "name": row[0],
                        "date": row[1],
                        "time": row[2]
                    })
    except:
        return jsonify([])

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)