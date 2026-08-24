import requests
import json
import sys

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

# Let's inspect OpenRouter specifically since it gave 200 on models
r = requests.get("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {key}"}, timeout=5)
print(f"OpenRouter Auth Check: {r.status_code} -> {r.text}", flush=True)

# Let's check Zhipu BigModel
try:
    r2 = requests.post(
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": "glm-4-flash", "messages": [{"role": "user", "content": "hi"}]},
        timeout=5
    )
    print(f"Zhipu chat: {r2.status_code} -> {r2.text}", flush=True)
except Exception as e:
    print(f"Zhipu chat err: {e}", flush=True)
