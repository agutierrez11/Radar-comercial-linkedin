import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"
base_url = "https://api-inference.modelscope.cn/v1"

# 1. Fetch available models
print("=== FETCHING MODELS FROM MODELSCOPE ===", flush=True)
r = requests.get(f"{base_url}/models", headers={"Authorization": f"Bearer {key}"}, timeout=8)
print(f"Status: {r.status_code}", flush=True)
if r.status_code == 200:
    data = r.json().get("data", [])
    print(f"Total models: {len(data)}", flush=True)
    qwen_models = [m['id'] for m in data if 'qwen' in m['id'].lower()]
    print(f"Qwen models ({len(qwen_models)}):")
    for qm in qwen_models:
        print(f" - {qm}", flush=True)

# 2. Test chat completion with Qwen
for qm in (qwen_models[:3] if qwen_models else ["Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "qwen/Qwen2.5-72B-Instruct"]):
    print(f"\n--- TESTING CHAT COMPLETION CON {qm} ---", flush=True)
    try:
        payload = {
            "model": qm,
            "messages": [
                {"role": "system", "content": "Eres un redactor comercial B2B de élite."},
                {"role": "user", "content": "Genera 1 frase de apertura para un VP de Pagos en LinkedIn."}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        r2 = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload,
            timeout=12
        )
        print(f"Status: {r2.status_code}", flush=True)
        if r2.status_code == 200:
            content = r2.json()['choices'][0]['message']['content']
            print(f"🎉 SUCCESS ({qm}):\n{content.strip()}", flush=True)
        else:
            print(f"Detalle: {r2.text[:200]}", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
