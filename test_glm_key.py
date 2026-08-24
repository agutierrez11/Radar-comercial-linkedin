import requests
import json

api_key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

endpoints = [
    ("Zhipu BigModel", "https://open.bigmodel.cn/api/paas/v4/chat/completions", "glm-4"),
    ("SiliconFlow", "https://api.siliconflow.cn/v1/chat/completions", "THUDM/glm-4-9b-chat"),
    ("SiliconFlow Qwen", "https://api.siliconflow.cn/v1/chat/completions", "Qwen/Qwen2.5-7B-Instruct"),
    ("OpenAI compatible standard / models", "https://open.bigmodel.cn/api/paas/v4/models", None),
    ("Siliconflow models", "https://api.siliconflow.cn/v1/models", None),
    ("DeepSeek / general proxy", "https://api.deepseek.com/v1/models", None),
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

for name, url, model in endpoints:
    print(f"Testing {name} -> {url}...")
    try:
        if model:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Hola, responde 'OK'"}],
                "max_tokens": 10
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=5)
            print(f"[{name}] Status: {resp.status_code}, Resp: {resp.text[:200]}")
        else:
            resp = requests.get(url, headers=headers, timeout=5)
            print(f"[{name}] Status: {resp.status_code}, Resp: {resp.text[:200]}")
    except Exception as e:
        print(f"[{name}] Error: {e}")
