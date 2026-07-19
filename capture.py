import cv2
import time
import os
import argparse
from model import size

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--count", type=int, default=200)
parser.add_argument("--camera-index", type=int, default=0)
parser.add_argument("--interval", type=float, default=0.15)
args = parser.parse_args()

cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
faceFinder = cv2.CascadeClassifier(cascadePath)
cap = cv2.VideoCapture(args.camera_index, cv2.CAP_DSHOW)

outDir = f"./dataset/{args.name}"
os.makedirs(outDir, exist_ok=True)
existing = len([i for i in os.listdir(outDir) if i.endswith(".png")])

lastCaptureTime = time.time()
saved = 0

if not cap.isOpened():
    raise RuntimeError("no cam")

while saved < args.count:
    ok, frame = cap.read()
    if not ok:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceFinder.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(120, 120))
    
    display = frame.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(display, (x,y), (x+w, y+h), (0, 255, 0), 2)

    if len(faces) == 1 and (time.time() - lastCaptureTime) >= args.interval:
        x, y, w, h = faces[0]
        faceCrop = gray[y:y + h, x:x + w]
        faceResized = cv2.resize(faceCrop, (size, size))
        filename = os.path.join(outDir, f"{existing + saved:04d}.png")
        cv2.imwrite(filename, faceResized)
        saved += 1
        lastCaptureTime = time.time()

    cv2.putText(display, f"saved: {saved}/{args.count}", (10,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("capture", display)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()