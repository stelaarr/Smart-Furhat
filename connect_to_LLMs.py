from furhat_remote_api import FurhatRemoteAPI
import google.generativeai as genai
import gestures_definitions

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
            # furhat.say(text="I couldn't hear you. Could you please repeat?")
            return None
    except Exception as e:
        print(f"Error during listening: {e}")
        # furhat.say(text="Something went wrong while listening. Could you try again?")
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

# Furhat 執行表情
def perform_emotion_gesture(emotion):
    try:
        if emotion == "happy":
            gestures_definitions.Perform_HappyExpression()
        elif emotion == "sad":
            gestures_definitions.Perform_SadExpression()
        elif emotion == "angry":
            gestures_definitions.Perform_AngryExpression()
        elif emotion == "surprised":
            gestures_definitions.Perform_SurprisedExpression()
        elif emotion == "disgust":
            gestures_definitions.Perform_DisgustExpression()
        elif emotion == "fear":
            gestures_definitions.Perform_FearExpression()
        else:
            gestures_definitions.Perform_NeutralExpression()
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
    # 構造 Prompt，包含對話歷史
    conversation_history.append(f"User ({user_emotion}): {user_speech}")
    history_text = "\n".join(conversation_history[-10:])  # 保留最近10條對話

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

    # 調用 LLM
    llm_response = call_gemini_api(prompt)
    print("LLM Response:", llm_response)

    # Furhat 說出回應
    furhat.say(text=llm_response)
    conversation_history.append(f"Bartender: {llm_response}")

    # 執行表情同步
    perform_emotion_gesture(user_emotion)
