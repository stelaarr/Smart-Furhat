import cv2
import torch
import threading
import time
from PIL import Image
from approach.PreData import REN_get_item
from furhat_remote_api import FurhatRemoteAPI
import google.generativeai as genai

# =====================
# Global Variables
# =====================
running = True                 # Used to control loop termination
current_emotion = "neutral"    # Store the currently detected emotion
last_faces = []  # Cache for face coordinates
frame_count = 0
FRAME_INTERVAL = 50            # Analyze emotion every 50 frames
conversation_history = []

# =====================
# Initialize resources
# =====================
cap = cv2.VideoCapture(0)
labels, device, model, transform, face_tracker = REN_get_item()

api_key = 'AIzaSyCLhiQiYG5lkWEEXacUYyzqoLMm-xdTFpc'  
genai.configure(api_key=api_key)
furhat = FurhatRemoteAPI("localhost")

furhat.say(text="Welcome! Good to see you tonight. Take a seat wherever you like. How’s your day been so far?")

# =====================
# Define Furhat Expressions
# =====================
def Perform_AngryExpression():
    furhat.gesture(body={
        "frames": [
            {
                "time": [1.0,2,2.2],
                "persist": True,
                "params": {
                    "BROW_In_LEFT":1.0,
                    "BROW_In_RIGHT":1.0,
                    "EXPR_ANGER": 1.0,
                    "NECK_TILT": 5
                }
            },
            {
                "time": [5.0],
                "persist": False,
                "params": {"reset": True}
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_DisgustExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0,2.0],
              "persist":True,
              "params":{
                "BROW_IN_LEFT":1,
                "BROW_IN_RIGHT":1,
                "NECK_ROLL":8.0,
                "EXPR_DISGUST":1
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_FearExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0,1,5,1.5,2.0],
              "persist":True,
              "params":{
                "BROW_IN_LEFT":1,
                "BROW_IN_RIGHT":1,
                "LOOK_DOWN":0.35,
                "EXPR_FEAR":1.0,
                "NECK_PAN":15
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_HappyExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0,1.5],
              "persist":False,
              "params":{
                "BROW_UP_LEFT":1,
                "BROW_UP_RIGHT":1,
                "SMILE_OPEN":0.8,
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_NeutralExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0],
              "persist":False,
              "params":{
                "PHONE_B_M_P": 1.0,
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_SadExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0,2.0,3.0,3.25,3.25],
              "persist":False,
              "params":{
                "SMILE_CLOSED":1.0,
                "EXPR_SAD": 1.0,
                "BROW_DOWN_LEFT":0.8,
                "BROW_DOWN_RIGHT":0.8,
                "LOOK_DOWN":0.2,
                "NECK_TILT":10
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def Perform_SurprisedExpression():
    furhat.gesture(body={
        "frames":[
            {
              "time":[1.0,1.5,1.5],
              "persist":True,
              "params":{
                "SURPRISE": 1.0,
                "BROW_UP_LEFT":1.0,
                "BROW_UP_RIGHT":1.0,
                "NECK_TILT":-8
              }
            },
            {
              "time":[5.0],
              "persist":False,
              "params":{
                "reset":True
              }
            }
        ],
        "class": "furhatos.gestures.Gesture"
    })

def perform_emotion_gesture(emotion):
    try:
        if emotion == "happy":
            Perform_HappyExpression()
        elif emotion == "sad":
            Perform_SadExpression()
        elif emotion == "angry":
            Perform_AngryExpression()
        elif emotion == "surprised":
            Perform_SurprisedExpression()
        elif emotion == "disgust":
            Perform_DisgustExpression()
        elif emotion == "fear":
            Perform_FearExpression()
        else:
            Perform_NeutralExpression()
    except Exception as e:
        print(f"Error performing gesture: {e}")

# =====================
# LLM function
# =====================
def call_gemini_api(prompt):
    try:
        model_gen = genai.GenerativeModel('gemini-pro')
        response = model_gen.generate_content(prompt)
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            raise ValueError("Empty or invalid response from Gemini API")
    except Exception as e:
        print(f"Error calling Google Gemini API: {e}")
        return "Sorry, I encountered an issue and couldn't process your request."

# =====================
# Camera Thread
# =====================
def camera_loop():
    global running, frame_count, current_emotion, last_faces,FRAME_INTERVAL
    print("[Camera Thread] Started.")
    while running:
        ret, frame = cap.read()
        if not ret:
            print("[Camera Thread] No frame captured.")
            break

        # Display the webcam feed
        cv2.imshow("Webcam", frame)

        # Perform emotion detection every FRAME_INTERVAL frames
        frame_count += 1
        if frame_count % FRAME_INTERVAL == 0:
            try:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_tracker.detectMultiScale(gray_frame)
                if len(faces) > 0:
                    (x1, y1, w, h) = faces[0]
                    last_faces = faces
                    face_frame = frame[y1:y1+h, x1:x1+w]
                    face_frame_tensor = transform(Image.fromarray(face_frame)).unsqueeze(0).to(device)
                    with torch.no_grad():
                        output = model(face_frame_tensor)
                        dominant_emotion = labels[torch.argmax(output, 1).item()]
                    current_emotion = dominant_emotion.lower()
                    print(f"[Camera Thread] Detected Emotion: {current_emotion}")
                else:
                    # If no face is detected, keep the current emotion
                    pass
            except Exception as e:
                print(f"[Camera Thread] Error analyzing emotion: {e}")
        if len(last_faces)>0:
            x, y, w, h = last_faces[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle
            cv2.putText(frame, current_emotion.capitalize(), (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Emotion text

                # Display the webcam feed with annotations
        cv2.imshow("Webcam", frame)

        # Check if 'q' is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    print("[Camera Thread] Exiting.")
    cap.release()
    cv2.destroyAllWindows()

# =====================
# Main Loop (Furhat & LLM)
# =====================
def main_loop():
    global running
    print("[Main Thread] Started.")

    while running:
        # Blocking call to Furhat listen
        response = furhat.listen()
        if not running:
            break

        if response.success and response.message:
            user_speech = response.message
            print("[Main Thread] User said:", user_speech)

            if "bye" in user_speech.lower():
                furhat.say(text="Goodbye! Have a nice day!")
                running = False
                break

            # Add user's speech and current emotion to conversation history
            conversation_history.append(f"User (Emotion: {current_emotion}): {user_speech}")
            history_text = "\n".join(conversation_history[-10:])

            prompt = f"""
            You are a friendly and empathetic bartender in a cozy bar. The user speaks and you also detect their emotion.
            Below is the conversation history, which includes the user's emotion and their message.

            Conversation history:
            {history_text}

            The user's current emotion is: {current_emotion}

            Your task:
            - Consider the user's last message and their emotion.
            - Provide a suitable, concise response to the user in one line of text.
            - On the next line, output the best emotion (among: happy, sad, surprised, fear, disgust, neutral, angry) 
              that Furhat should display when responding.

            Output format:
            Line 1: The reply text Furhat should say to the user.
            Line 2: The chosen emotion for Furhat to display.
            """

            llm_response = call_gemini_api(prompt)
            print("[Main Thread] LLM Response (raw):", llm_response)

            # Split LLM response
            lines = llm_response.split('\n')
            if len(lines) < 2:
                furhat_text = "Sorry, I didn't understand that."
                furhat_emotion = "neutral"
            else:
                furhat_text = lines[0].strip()
                furhat_emotion = lines[1].strip().lower()

            allowed_emotions = ["happy", "sad", "surprised", "fear", "disgust", "neutral", "angry"]
            if furhat_emotion not in allowed_emotions:
                furhat_emotion = "neutral"

            # Furhat speaks and shows emotion
            furhat.say(text=furhat_text)
            conversation_history.append(f"Bartender: {furhat_text} (Emotion: {furhat_emotion})")
            perform_emotion_gesture(furhat_emotion)
        else:
            # If no speech detected, just wait a bit
            time.sleep(0.1)

    print("[Main Thread] Exiting.")

if __name__ == "__main__":
    # Start camera thread
    camera_thread = threading.Thread(target=camera_loop, daemon=True)
    camera_thread.start()

    # Run main loop in main thread
    main_loop()

    # When main_loop finishes, stop camera thread
    running = False
    camera_thread.join()
    print("[System] All threads stopped. Program finished.")
