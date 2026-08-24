import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"
base_url = "https://zenmux.ai/api/v1"

# Let's test the free models and various Qwen / GLM / Deepseek models
models_to_test = [
    "z-ai/glm-5.3-free",
    "z-ai/glm-4.7-flash-free",
    "z-ai/glm-4.6v-flash-free",
    "qwen/qwen3.7-flash",
    "qwen/qwen3.5-flash",
    "qwen/qwen3-14b",
    "z-ai/glm-5.2",
    "z-ai/glm-5.3",
    "deepseek/deepseek-chat",
    "meta-llama/llama-3.3-70b-instruct"
]

print("=== PROBANDO MODELOS ACTIVOS EN ZENMUX ===", flush=True)

working_models = []

for mod in models_to_test:
    payload = {
        "model": mod,
        "messages": [
            {"role": "system", "content": "Eres un asistente de ventas B2B."},
            {"role": "user", "content": "Genera 1 frase de apertura para prospectar a un VP de Pagos."}
        ],
        "max_tokens": 60
    }
    try:
        r = requests.post(f"{base_url}/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=payload, timeout=10)
        if r.status_code == 200:
            res_json = r.json()
            content = res_json['choices'][0]['message']['content']
            print(f"\n✅ [FUNCIONA]: {mod}")
            print(f"Respuesta: {content.strip()}")
            working_models.append(mod)
        else:
            print(f"\n❌ [{mod}] Status {r.status_code}: {r.text[:120]}")
    except Exception as e:
        print(f"\n⚠️ [{mod}] Error: {e}")

print(f"\n=== MODELOS LISTOS PARA USAR: {working_models} ===")
