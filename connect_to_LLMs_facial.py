from furhat_remote_api import FurhatRemoteAPI
import google.generativeai as genai

# Set up Google Gemini API
api_key = 'AIzaSyCLhiQiYG5lkWEEXacUYyzqoLMm-xdTFpc'  
genai.configure(api_key=api_key)

# Initialize Furhat
furhat = FurhatRemoteAPI("localhost")
furhat.say(text="Welcome! Good to see you tonight. Take a seat wherever you like. How’s your day been so far?")

# Initialize conversation history
conversation_history = []

# Simulate detecting user emotion
def detect_user_emotion():
    return "angry"  # Simulated emotion (can be expanded)

# Receive user input
def get_user_input():
    try:
        response = furhat.listen()
        if response.success and response.message:
            return response.message
        else:
            return None
    except Exception as e:
        print(f"Error during listening: {e}")
        return None

# Call LLM (Google Gemini API)
def call_gemini_api(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            raise ValueError("Empty or invalid response from Gemini API")
    except Exception as e:
        print(f"Error calling Google Gemini API: {e}")
        return "Sorry, I encountered an issue and couldn't process your request."

# Define functions for facial expressions
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
        }],
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
        }],
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
        }],
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
        }],
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
        }],
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
        }],
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
        }],
        "class": "furhatos.gestures.Gesture"
    })

# Execute expressions with Furhat
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


# Main logic
while True:
    # Detect user emotion
    user_emotion = detect_user_emotion()
    print("Detected user emotion:", user_emotion)

    # Get user speech input
    user_speech = get_user_input()
    if not user_speech:
        continue  # Skip this round if user input is not successfully received

    print("User said:", user_speech)
    # Check exit condition
    if "bye" in user_speech.lower():
        furhat.say(text="Goodbye! Have a nice day!")
        break
    
    # Add user's message and emotion to conversation history
    conversation_history.append(f"User (Emotion: {user_emotion}): {user_speech}")
    history_text = "\n".join(conversation_history[-10:])  # Keep the last 10 lines of conversation
    
    # Modify prompt to request LLM to generate both text responses and expressions
    prompt = f"""
    You are a friendly and empathetic bartender in a cozy bar. The user speaks and you also detect their emotion.
    Below is the conversation history, which includes the user's emotion and their message.

    Conversation history:
    {history_text}

    The user's current emotion is: {user_emotion}

    Your task:
    - Consider the user's last message and their emotion.
    - Provide a suitable, concise response to the user in one line of text.
    - On the next line, output the best emotion (among: happy, sad, surprised, fear, disgust, neutral) that Furhat should display when responding.

    Output format:
    Line 1: The reply text Furhat should say to the user.
    Line 2: The chosen emotion for Furhat to display.

    Make sure the second line is just one of the allowed emotions.
    """

    # Call LLM
    llm_response = call_gemini_api(prompt)
    print("LLM Response (raw):", llm_response)

    # Split LLM response into two lines
    lines = llm_response.split('\n')
    if len(lines) < 2:
        # Provide default values if response does not have two lines
        furhat_text = "Sorry, I didn't understand that."
        furhat_emotion = "neutral"
    else:
        furhat_text = lines[0].strip()
        furhat_emotion = lines[1].strip().lower()
    
    # Ensure the expression output is one of the expected ones
    allowed_emotions = ["happy", "sad", "surprised", "fear", "disgust", "neutral", "angry"]
    if furhat_emotion not in allowed_emotions:
        furhat_emotion = "neutral"

    # Furhat speaks the response
    furhat.say(text=furhat_text)
    conversation_history.append(f"Bartender: {furhat_text} (Emotion: {furhat_emotion})")

    # Execute emotion gesture synchronously
    perform_emotion_gesture(furhat_emotion)
