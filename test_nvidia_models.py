import requests
import json

key = "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"

models = [
    "meta/llama-3.3-70b-instruct",
    "meta/llama3-70b-instruct",
    "deepseek-ai/deepseek-r1",
    "mistralai/mistral-large-2-instruct",
    "nvidia/neva-22b"
]

url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

for m in models:
    print(f"Probando modelo NVIDIA: {m}...")
    payload = {
        "model": m,
        "messages": [{"role": "user", "content": "Hola, responde brevemente en español confirmando conexión."}],
        "temperature": 0.5,
        "max_tokens": 80
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"  Status Code: {r.status_code}")
        if r.status_code == 200:
            res = r.json()
            print(f"  ✅ ÉXITO TOTAL CON MODELO {m}!")
            print("  Respuesta:", res["choices"][0]["message"]["content"])
            break
        else:
            print("  Error:", r.text[:120])
    except Exception as e:
        print("  Exception:", e)
