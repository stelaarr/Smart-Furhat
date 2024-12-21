import cv2
import torch
from approach.PreData import REN_get_item
from PIL import Image
# Parameters
FRAME_INTERVAL = 50  # Analyze every 50th frame

# Initialize webcam
cap = cv2.VideoCapture(0)

# Load pre-trained model and parameters
labels, device, model, transform, face_tracker = REN_get_item()

# Variables to store results
emotion_buffer = []
frame_count = 0

print("Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process every FRAME_INTERVAL-th frame
    frame_count += 1
    if frame_count % FRAME_INTERVAL == 0:
        try:
            # Detect facebox
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_tracker.detectMultiScale(gray_frame) 
            for (x1, y1, w, h) in faces:
                face_frame = frame[y1:y1+h, x1:x1+w]
                
                # Use ResEmoteNet to detect emotion
                face_frame_tensor = transform(Image.fromarray(face_frame)).unsqueeze(0).to(device)
                with torch.no_grad():
                    output = model(face_frame_tensor)
                    dominant_emotion = labels[torch.argmax(output, 1).item()]
                break
            print(f"Detected Emotion: {dominant_emotion}")

            # Store emotion for smoothing
            emotion_buffer.append(dominant_emotion)

        except Exception as e:
            print(f"Error analyzing emotion: {e}")

    # Display webcam feed
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()