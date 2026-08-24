import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"
base_url = "https://zenmux.ai/api/v1"

# 1. List available models
print("--- FETCHING MODELS FROM ZENMUX ---", flush=True)
try:
    r_models = requests.get(f"{base_url}/models", headers={"Authorization": f"Bearer {key}"}, timeout=8)
    print(f"Status: {r_models.status_code}", flush=True)
    if r_models.status_code == 200:
        models_data = r_models.json().get("data", [])
        print(f"Total models available: {len(models_data)}", flush=True)
        # Search for qwen and glm
        for m in models_data:
            m_id = m.get("id", "")
            if any(k in m_id.lower() for k in ["qwen", "glm", "z-ai", "thudm"]):
                print(f" - Model: {m_id}", flush=True)
    else:
        print(f"Error: {r_models.text}", flush=True)
except Exception as e:
    print(f"Err: {e}", flush=True)

# 2. Test chat completion with GLM and Qwen
test_models = ["glm-5.2", "Qwen/Qwen3.8-27B", "z-ai/glm-5", "qwen/qwen-2.5-72b-instruct"]

for mod in test_models:
    print(f"\n--- TESTING CHAT WITH {mod} ---", flush=True)
    try:
        payload = {
            "model": mod,
            "messages": [
                {"role": "system", "content": "Eres un asistente de ventas B2B experto."},
                {"role": "user", "content": "Genera 1 frase potente de apertura para un VP de Pagos en Fintech."}
            ],
            "max_tokens": 100
        }
        r_chat = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=12)
        print(f"Status: {r_chat.status_code}", flush=True)
        if r_chat.status_code == 200:
            content = r_chat.json()["choices"][0]["message"]["content"]
            print(f"Response ({mod}):\n{content}", flush=True)
        else:
            print(f"Failed: {r_chat.text}", flush=True)
    except Exception as e:
        print(f"Err chat: {e}", flush=True)
