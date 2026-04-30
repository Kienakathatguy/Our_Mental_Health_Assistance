import os
from google import genai

def call_chatbot_api(messages):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Chưa cấu hình GEMINI_API_KEY."

    client = genai.Client(api_key=api_key)

    try:
        prompt = "Bạn là trợ lý tâm lý...\n\n"

        for msg in messages:
            if msg["role"] == "user":
                prompt += f"User: {msg['content']}\n"
            else:
                prompt += f"Assistant: {msg['content']}\n"

        prompt += "Assistant:"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini ERROR:", e)
        return "😢 Chatbot lỗi rồi."