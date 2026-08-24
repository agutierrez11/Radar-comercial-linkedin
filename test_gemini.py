import os
import requests
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"

r = requests.post(
    url,
    headers={"Content-Type": "application/json"},
    json={"contents": [{"parts": [{"text": "Di 'Gemini listo para la demo'"}]}]},
    timeout=6
)
print(f"Gemini Status: {r.status_code}")
if r.status_code == 200:
    print(r.json()['candidates'][0]['content']['parts'][0]['text'])
else:
    print(r.text)
