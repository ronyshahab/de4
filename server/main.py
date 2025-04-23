from flask import Flask, request
from flask_cors import CORS
import threading
import os

from test import face_verify, stop_verification

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part', 400

    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return 'File uploaded successfully', 200

@app.route("/start", methods=["GET"])
def start_verification():
 threading.Thread(target=face_verify).start()
 return "Face verification started"

@app.route("/stop", methods=["GET"])
def stop_verification_route():
    stop_verification()
    return "Verification stopped."

if __name__ == '__main__':
    app.run(debug=True)
