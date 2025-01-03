import cv2
import opencv_jupyter_ui as jcv2
from feat import Detector
from IPython.display import Image
import numpy as np
import torch
import os
from approach.ResEmoteNet import ResEmoteNet
from torchvision import transforms
from PIL import Image


labels = ['happy','surprise','sad','angry','disgust','fear','neutral']
device = "cuda" if torch.cuda.is_available() else "cpu"
model = ResEmoteNet()
model.load_state_dict(torch.load('.//checkpoints//best_modelBS32.pth', weights_only=True))
model.to(device)
model.eval()
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# detector = Detector(device="cuda")  # 初始化偵測器
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("can't not open camera")
    exit()
face_tracker = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    if not ret:
        print("can't not return screen")
        break
        
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detected_faces = detector.detect_faces(frame)
    faces = face_tracker.detectMultiScale(gray_frame) 
    for (x1, y1, w, h) in faces:
        print(faces)
        x1 = int(x1)
        y1 = int(y1)
        w = int(w)
        h = int(h)
        face_frame = frame[y1:y1+h, x1:x1+w]
        face_frameImage = Image.fromarray(face_frame)
        face_frameImage = transform(face_frameImage).unsqueeze(0).to(device)
        cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), (0, 255, 0), 5)
        with torch.no_grad():
            output = model(face_frameImage)
            _, predicted = torch.max(output, 1)
        predicted_label = labels[predicted.item()]
        # detected_landmarks = detector.detect_landmarks(frame, detected_faces)
        # face_result = detector.detect_emotions(frame, detected_faces, detected_landmarks)

        
        text = predicted_label

        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (36, 255, 12), 2)
        break

    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
