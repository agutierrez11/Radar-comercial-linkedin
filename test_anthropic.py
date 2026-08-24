import os
import requests
from dotenv import load_dotenv

load_dotenv()
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

r = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": anthropic_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    json={
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 50,
        "messages": [{"role": "user", "content": "Di 'Claude listo para la demo'"}]
    },
    timeout=6
)
print(f"Claude Status: {r.status_code}")
if r.status_code == 200:
    print(r.json()['content'][0]['text'])
else:
    print(r.text)
