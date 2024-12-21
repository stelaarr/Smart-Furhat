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
current_emotion = "neutral"  
last_faces = []  # Cache for face coordinates
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

            if len(faces)>0:
                (x1, y1, w, h) = faces[0]
                last_faces = faces
                face_frame = frame[y1:y1+h, x1:x1+w]
                # Use ResEmoteNet to detect emotion
                face_frame_tensor = transform(Image.fromarray(face_frame)).unsqueeze(0).to(device)
                with torch.no_grad():
                    output = model(face_frame_tensor)
                    dominant_emotion = labels[torch.argmax(output, 1).item()]
                current_emotion = dominant_emotion.lower()
                print(f"Detected Emotion: {current_emotion}")
                # Store emotion for smoothing
                emotion_buffer.append(current_emotion)
            else:
                pass

        except Exception as e:
            print(f"Error analyzing emotion: {e}")

    # Draw rectangles and display emotions if faces are detected
    if len(last_faces)>0:
        x, y, w, h = last_faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle
        cv2.putText(frame, current_emotion.capitalize(), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Emotion text

            # Display the webcam feed with annotations
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()