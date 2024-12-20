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
    return "angry"  # Simulate emotion (can be extended)

# Receive user input
def get_user_input():
    try:
        response = furhat.listen()
        if response.success and response.message:
            return response.message
        else:
            # furhat.say(text="I couldn't hear you. Could you please repeat?")
            return None
    except Exception as e:
        print(f"Error during listening: {e}")
        # furhat.say(text="Something went wrong while listening. Could you try again?")
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

# Angry expression
def Perform_AngryExpression():
    furhat.gesture(body={
    "frames": [
    {
        "time": [1.0,2,2.2],    # A list of times can be provided, at those times the params will be executed.
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

# Disgust expression
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

# Fear expression
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

# Happy expression
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

# Neutral expression
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

# Sad expression
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

# Surprise expression
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

# Furhat performs expressions
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
    # Construct prompt, including conversation history
    conversation_history.append(f"User ({user_emotion}): {user_speech}")
    history_text = "\n".join(conversation_history[-10:])  # Keep the last 10 lines of conversation

    prompt = f"""
    You are a friendly and empathetic bartender in a cozy bar. Continue the conversation with the user below. Make sure your response is coherent and keeps the context of the previous exchanges.

    Conversation history:
    {history_text}

    Your task:
    - Recommend a suitable drink for the user if they don't specify one.
    - Engage in a warm, casual conversation to make the user feel welcome.
    - If the user seems unhappy or stressed, listen to their concerns and offer comforting responses.

    Respond concisely with at most two sentences.
    """

    # Call LLM
    llm_response = call_gemini_api(prompt)
    print("LLM Response:", llm_response)

    # Furhat speaks the response
    furhat.say(text=llm_response)
    conversation_history.append(f"Bartender: {llm_response}")

    # Perform expression synchronization
    perform_emotion_gesture(user_emotion)
