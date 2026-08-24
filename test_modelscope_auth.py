import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"
url = "https://api-inference.modelscope.cn/v1/chat/completions"
model = "Qwen/Qwen3.8-27B"

payload = {
    "model": model,
    "messages": [{"role": "user", "content": "Di 'OK'"}],
    "max_tokens": 20
}

# Test different auth headers for ModelScope
auth_variants = [
    ("Bearer token", {"Authorization": f"Bearer {key}"}),
    ("Direct token in Auth", {"Authorization": key}),
    ("X-ModelScope-Token", {"X-ModelScope-Token": key}),
    ("Both headers", {"Authorization": f"Bearer {key}", "X-ModelScope-Token": key}),
    ("Header token", {"token": key}),
    ("DashScope header", {"X-DashScope-ApiKey": key}),
]

for name, hdr in auth_variants:
    hdr["Content-Type"] = "application/json"
    print(f"Probando {name}...", flush=True)
    try:
        r = requests.post(url, headers=hdr, json=payload, timeout=6)
        print(f" -> Status: {r.status_code}, Body: {r.text[:140]}", flush=True)
    except Exception as e:
        print(f" -> Error: {e}", flush=True)
