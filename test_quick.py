import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"
base_url = "https://zenmux.ai/api/v1"

models = ["z-ai/glm-5.3-free", "z-ai/glm-4.7-flash-free", "z-ai/glm-4.6v-flash-free", "z-ai/glm-5.2", "qwen/qwen3.8-max", "qwen/qwen3.7-flash"]

for m in models:
    print(f"Testing {m}...", flush=True)
    try:
        payload = {
            "model": m,
            "messages": [{"role": "user", "content": "Di 'OK'"}],
            "max_tokens": 10
        }
        r = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=6)
        print(f" -> Status: {r.status_code}, Body: {r.text[:120]}", flush=True)
    except Exception as e:
        print(f" -> Error: {e}", flush=True)
