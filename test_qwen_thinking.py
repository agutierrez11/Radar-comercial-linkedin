import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"
base_url = "https://llm.disier.net/v1"

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Qwen/Qwen3.8-27B",
    "messages": [
        {"role": "system", "content": "Eres un asistente."},
        {"role": "user", "content": "Di exactamente: HOLA"}
    ],
    "max_tokens": 1000
}

try:
    r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=25)
    print("Status:", r.status_code, flush=True)
    res = r.json()
    print("Keys in JSON:", list(res.keys()), flush=True)
    choice = res.get("choices", [{}])[0]
    msg = choice.get("message", {})
    print("Message keys:", list(msg.keys()), flush=True)
    print("Reasoning Content:", msg.get("reasoning_content"), flush=True)
    print("Content:", msg.get("content"), flush=True)
except Exception as e:
    print("Error:", e, flush=True)
