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
        {"role": "system", "content": "Eres un redactor B2B."},
        {"role": "user", "content": "Di 'HOLA, QWEN 3.8 FUNCIONA PERFECTO'"}
    ],
    "max_tokens": 100
}

r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=15)
print(f"Status: {r.status_code}", flush=True)
print(f"Full JSON:\n{json.dumps(r.json(), indent=2)}", flush=True)
