import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta/llama-3.1-70b-instruct",
    "messages": [{"role": "user", "content": "Hola Llama 3.1 70B en NVIDIA NIM, confirma que estás activo respondiendo con un saludo efusivo para Antonio y Radar Comercial."}],
    "temperature": 0.5,
    "max_tokens": 100
}

r = requests.post(url, headers=headers, json=payload, timeout=10)
print(f"Status Code: {r.status_code}")
if r.status_code == 200:
    res = r.json()
    print("SUCCESS NVIDIA NIM Llama 3.1 70B:")
    print(res["choices"][0]["message"]["content"])
