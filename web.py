import face_recognition
from flask import Flask, jsonify, request
import os
import numpy
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)

face_path = os.environ['FACE_PATH']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    a = {"code": 200}
    return jsonify(a)


@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        result = {"code": 101, "message": "Missing parameter 'image'"}
        return jsonify(result)
    image = request.files['image']
    if image.filename == '':
        result = {"code": 102, "message": "Missing field 'filename' of parameter 'image'"}
        return jsonify(result)

    if image and allowed_file(image.filename):
        return detect_faces_in_image(image)

    result = {"code": 103, "message": "Invalid file extension"}
    return jsonify(result)


@app.route('/verify', methods=['POST'])
def verify():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
    else:
        data = request.form
    token1 = data.get("token1", "")
    token2 = data.get("token2", "")
    threshold = data.get("threshold", 0.4)
    if not token1:
        return jsonify({"code": 101, "message": "Missing parameter 'token1'"})

    if not token2:
        return jsonify({"code": 101, "message": "Missing parameter 'token2'"})

    return face_compare(token1, token2, threshold)


def face_compare(token1, token2, threshold):
    file_name1 = f"{face_path}/{token1}.txt"
    file_name2 = f"{face_path}/{token2}.txt"
    if not os.path.exists(file_name1):
        return jsonify({"code": 102, "message": "Invalid parameter 'token1'"})

    if not os.path.exists(file_name2):
        return jsonify({"code": 102, "message": "Invalid parameter 'token2'"})

    encoding1 = numpy.loadtxt(file_name1)
    encoding2 = numpy.loadtxt(file_name2)
    results = face_recognition.compare_faces([encoding1], encoding2, threshold)
    return jsonify({"code": 200, "data": {"result": bool(results[0])}})


def save_encodes(encoding):
    token = uuid.uuid4()
    file_name = f"{face_path}/{token}.txt"
    numpy.savetxt(file_name, encoding)
    return token


def detect_faces_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)
    face_encodings = face_recognition.face_encodings(img)

    # face_token = list(map(save_encodes, face_encodings))
    face_token = [save_encodes(x) for x in face_encodings]

    result = {"code": 200, "data": {
        "face_token": face_token
    }}
    return jsonify(result)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=os.environ['APP_PORT'], host='0.0.0.0')
