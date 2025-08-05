# models/llm.py
import requests
from config.config import GEMINI_API_KEY, DEEPSEEK_API_KEY, DEFAULT_MODEL, RESPONSE_MODE

def call_llm(prompt):
    if DEFAULT_MODEL == "gemini":
        return call_gemini(prompt)
    elif DEFAULT_MODEL == "deepseek":
        return call_deepseek(prompt)
    else:
        return "Error: Unsupported model selected."

import time

def call_gemini(prompt):
    try:
        time.sleep(1)  # ⏱️ Prevent rate limit
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        resp = requests.post(url, headers={"Content-Type": "application/json"}, params=params, json=data)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini API Error: {str(e)}"



def call_deepseek(prompt):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        data = {
            "model": "deepseek-coder",
            "messages": [
                {"role": "system", "content": "You are a helpful AI code assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"DeepSeek API Error: {str(e)}"
