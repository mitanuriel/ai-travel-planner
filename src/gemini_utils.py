import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load GEMINI_API_KEY from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini_api(prompt, model="models/gemini-1.5-flash-latest"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 200:
        response_json = resp.json()
        try:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "No result from Gemini."
    else:
        return f"Error: {resp.status_code} - {resp.text}"
