import os
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

for mod in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro-latest", "gemini-1.5-flash-8b"]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={gemini_key}"
    r = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": "Di 'OK'"}]}]},
        timeout=4
    )
    print(f"[{mod}] Status: {r.status_code} -> {r.text[:120]}")
