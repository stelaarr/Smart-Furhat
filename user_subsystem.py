import cv2
from deepface import DeepFace

# Parameters
FRAME_INTERVAL = 50  # Analyze every 50th frame

# Initialize webcam
cap = cv2.VideoCapture(0)

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
            # Change here to our Emotion Detection Model
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']
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