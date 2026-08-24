import requests
import json

key = "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"
url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

models_to_test = [
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-405b-instruct",
    "google/gemma-2-27b-it",
    "mistralai/mistral-7b-instruct-v0.3",
    "nvidia/llama-3.1-nemotron-70b-reward"
]

for m in models_to_test:
    print(f"Probando {m}...")
    payload = {
        "model": m,
        "messages": [{"role": "user", "content": "Hola responde en 5 palabras"}],
        "max_tokens": 50
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=8)
        print(f"  Code: {r.status_code}")
        if r.status_code == 200:
            res = r.json()
            print(f"  ✅ FUNCIONÓ PERFECTAMENTE CON {m}!")
            print("  Respuesta:", res["choices"][0]["message"]["content"])
            break
        else:
            print("  Respuesta error:", r.text[:100])
    except Exception as e:
        print("  Error exception:", e)
