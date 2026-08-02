import flask
import glob
import time
import threading
import cv2
from recognize_live import FaceRecognizer
from constants import camera_index, threshold

recognizer = FaceRecognizer(model_path="face_model.pt", camera_index=camera_index, threshold=threshold)

app = flask.Flask(__name__)

frame = None

def update_frame():
    global frame
    while True:
        frame = recognizer.recognizeWithFrame()
        if frame is not None:
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        time.sleep(0.02)

@app.route('/')

def index():
    return flask.Response(update_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=5000)