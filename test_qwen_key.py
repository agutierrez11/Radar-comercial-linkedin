import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"

endpoints = [
    ("DashScope Int (Alibaba)", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-plus"),
    ("DashScope China (Alibaba)", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-plus"),
    ("DashScope Qwen Turbo", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-turbo"),
    ("DashScope China Turbo", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-turbo"),
    ("DashScope Qwen 2.5", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen2.5-72b-instruct"),
    ("SiliconFlow", "https://api.siliconflow.cn/v1/chat/completions", "Qwen/Qwen2.5-7B-Instruct"),
    ("OpenRouter", "https://openrouter.ai/api/v1/chat/completions", "qwen/qwen-2.5-72b-instruct"),
    ("DeepInfra", "https://api.deepinfra.com/v1/openai/chat/completions", "Qwen/Qwen2.5-72B-Instruct"),
    ("Together", "https://api.together.xyz/v1/chat/completions", "Qwen/Qwen2.5-72B-Instruct"),
    ("Novita", "https://api.novita.ai/v3/openai/chat/completions", "qwen/qwen-2.5-72b-instruct"),
]

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [{"role": "user", "content": "Di 'QWEN ACTIVO'"}],
    "max_tokens": 30
}

print("=== PROBANDO API KEY DE QWEN ===", flush=True)

for name, url, model in endpoints:
    print(f"Probando {name} con modelo '{model}'...", flush=True)
    body = dict(payload)
    body["model"] = model
    try:
        r = requests.post(url, headers=headers, json=body, timeout=5)
        print(f" -> Status: {r.status_code}", flush=True)
        if r.status_code == 200:
            print(f"  🎉 SUCCESS! Respuesta: {r.json()['choices'][0]['message']['content']}", flush=True)
        else:
            print(f"  Detalle: {r.text[:140]}", flush=True)
    except Exception as e:
        print(f"  Error: {e}", flush=True)
