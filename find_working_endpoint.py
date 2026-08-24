import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

test_endpoints = [
    ("OpenRouter", "https://openrouter.ai/api/v1/chat/completions", ["qwen/qwen-2.5-72b-instruct", "z-ai/glm-4.5", "z-ai/glm-5.2", "thudm/glm-4-9b-chat"]),
    ("Zhipu BigModel", "https://open.bigmodel.cn/api/paas/v4/chat/completions", ["glm-4", "glm-4-flash"]),
    ("AiHubMix", "https://aihubmix.com/v1/chat/completions", ["glm-4", "glm-5.2", "Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen3.8-27B"]),
    ("Novita", "https://api.novita.ai/v3/openai/chat/completions", ["zai-org/glm-5.3", "qwen/qwen-2.5-72b-instruct"]),
    ("AiHub / OneAPI Proxy", "https://api.ai-v1.com/v1/chat/completions", ["glm-5.2", "Qwen/Qwen3.8-27B", "glm-4"]),
]

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

for provider, url, models in test_endpoints:
    print(f"\n================ Testing {provider} ================")
    for model in models:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Di 'FUNCIONA'"}],
            "max_tokens": 20
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=6)
            print(f"[{model}] Status: {r.status_code}")
            if r.status_code == 200:
                print(f" SUCCESS: {r.json()['choices'][0]['message']['content']}")
            else:
                print(f" Resp: {r.text[:200]}")
        except Exception as e:
            print(f"[{model}] Request failed: {e}")
