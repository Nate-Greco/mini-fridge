import cv2
import torch
import torch.nn.functional as F
import argparse
import time

from model import size, FaceCNN, get_device

def load_model(checkpoint_path, device):
    ckpt = torch.load(checkpoint_path, map_location="cpu")
    model = FaceCNN(num=len(ckpt["classes"]))
    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()
    return model, ckpt["classes"]

class FaceRecognizer:
    def __init__(self, model_path="face_model.pt", camera_index=1, threshold=0.9):
        self.device = torch.device("cpu")
        self.model, self.classes = load_model(model_path, self.device)
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.cap = cv2.VideoCapture(camera_index)
        self.threshold = threshold

        if not self.cap.isOpened():
            raise RuntimeError("no cam")
        
    def recognize(self):
        ok, frame = self.cap.read()
        if not ok:
            return None, 0.0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(120, 120))

        if len(faces) != 1:
            return None, 0.0
        
        x, y, w, h = faces[0]

        faceCrop = gray[y:y + h, x:x + w]
        faceResized = cv2.resize(faceCrop, (size, size)).astype("float32")
        faceNorm = (faceResized / 255.0 - 0.5) / 0.5

        tensor = torch.from_numpy(faceNorm).unsqueeze(0).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1)[0]
            conf, idx = torch.max(probs, dim=0)

        conf = conf.item()
        if conf >= self.threshold:
            return self.classes[idx.item()], conf
        return None, conf

    def recognizeWithFrame(self):
        ok, frame = self.cap.read()

        if not ok:
            return None, 0.0, None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(120, 120))

        display = frame.copy()

        if len(faces) != 1:
            return None, 0.0, display

        x, y, w, h = faces[0]
        faceCrop = gray[y:y + h, x:x + w]
        faceResized = cv2.resize(faceCrop, (size, size)).astype("float32")
        faceNorm = (faceResized / 255.0 - 0.5) / 0.5

        tensor = torch.from_numpy(faceNorm).unsqueeze(0).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1)[0]
            conf, idx = torch.max(probs, dim=0)

        conf = conf.item()
        name = self.classes[idx.item()] if conf >= self.threshold else None
        label = f"{name} ({conf:.2f})" if name else f"Unknown ({conf:.2f})"
        color = (0, 200, 0) if name else (200, 0, 0)
        cv2.rectangle(display, (x, y), (x + w, y+ h), color, 2)
        cv2.putText(display, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        for i, cls_name in enumerate(self.classes):
            probText = f"{cls_name}: {probs[i].item():.2f}"
            cv2.putText(display, probText, (10, 30 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        return display
        
    
    def close(self):
        self.cap.release()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", default="face_model.pt")
    parser.add_argument("--camera-index", type=int, default=1)
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()

    recognizer = FaceRecognizer(
        model_path=args.model_path,
        camera_index=args.camera_index,
        threshold=args.threshold,
    )

    try:
        while True:
            name, conf = recognizer.recognize()
            if name:
                print(f"recognized: {name} with {conf:.2f}")
            else:
                print(f"No confident match with {conf:.2f}")
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        recognizer.close()