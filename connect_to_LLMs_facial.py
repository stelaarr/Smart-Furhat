from furhat_remote_api import FurhatRemoteAPI
import google.generativeai as genai

# 設定 Google Gemini API
api_key = 'AIzaSyCLhiQiYG5lkWEEXacUYyzqoLMm-xdTFpc'  
genai.configure(api_key=api_key)

# 初始化 Furhat
furhat = FurhatRemoteAPI("localhost")
furhat.say(text="Welcome! Good to see you tonight. Take a seat wherever you like. How’s your day been so far?")

# 初始化對話歷史
conversation_history = []

# 模擬偵測使用者表情
def detect_user_emotion():
    return "angry"  # 模擬情緒（可擴展）

# 接收用戶輸入
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

# 呼叫 LLM（Google Gemini API）
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

# 表情函數定義（略，與你上面提供的一樣）
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

# Furhat 執行表情
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


# 主邏輯
while True:
    # 偵測使用者情緒
    user_emotion = detect_user_emotion()
    print("Detected user emotion:", user_emotion)

    # 獲取用戶語音輸入
    user_speech = get_user_input()
    if not user_speech:
        continue  # 如果未成功獲取用戶輸入，跳過本輪

    print("User said:", user_speech)
    # 檢查結束條件
    if "bye" in user_speech.lower():
        furhat.say(text="Goodbye! Have a nice day!")
        break
    
    # 將使用者的語句與情緒加入歷史
    conversation_history.append(f"User (Emotion: {user_emotion}): {user_speech}")
    history_text = "\n".join(conversation_history[-10:])  # 保留最近10條對話
    
    # 修改 prompt，要求 LLM 同時產生文字回應與表情
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

    # 調用 LLM
    llm_response = call_gemini_api(prompt)
    print("LLM Response (raw):", llm_response)

    # 將 LLM 回覆分成兩行
    lines = llm_response.split('\n')
    if len(lines) < 2:
        # 如果沒拿到兩行，則給預設值
        furhat_text = "Sorry, I didn't understand that."
        furhat_emotion = "neutral"
    else:
        furhat_text = lines[0].strip()
        furhat_emotion = lines[1].strip().lower()
    
    # 確保表情輸出是預期之一
    allowed_emotions = ["happy", "sad", "surprised", "fear", "disgust", "neutral", "angry"]
    if furhat_emotion not in allowed_emotions:
        furhat_emotion = "neutral"

    # Furhat 說出回應
    furhat.say(text=furhat_text)
    conversation_history.append(f"Bartender: {furhat_text} (Emotion: {furhat_emotion})")

    # 執行表情同步
    perform_emotion_gesture(furhat_emotion)
