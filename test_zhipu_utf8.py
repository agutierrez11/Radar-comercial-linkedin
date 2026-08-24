import requests
import json
import sys

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# Try different model names
models_to_test = ["glm-4", "glm-4-flash", "glm-4-air", "glm-4-plus", "glm-5", "glm-5.2", "Qwen/Qwen3.8-27B", "glm-4-0520"]

for model in models_to_test:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hola, responde brevemente en español: ¿Cuál es tu nombre de modelo?"}],
        "max_tokens": 50
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=8)
        print(f"[{model}] Status: {r.status_code}")
        print(f"Response: {r.text[:300]}")
    except Exception as e:
        print(f"[{model}] Error: {e}")
