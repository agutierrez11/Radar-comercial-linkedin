import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"
base_url = "https://llm.disier.net/v1"

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# 1. Test /v1/models
print("=== 1. LISTANDO MODELOS EN DISIER ===", flush=True)
try:
    r_models = requests.get(f"{base_url}/models", headers=headers, timeout=8)
    print(f"Status: {r_models.status_code}", flush=True)
    if r_models.status_code == 200:
        print(f"Modelos:\n{json.dumps(r_models.json(), indent=2)}", flush=True)
    else:
        print(f"Error: {r_models.text}", flush=True)
except Exception as e:
    print(f"Err /models: {e}", flush=True)

# 2. Test Qwen/Qwen3.8-27B Chat Completion
print("\n=== 2. PROBANDO CHAT COMPLETION CON Qwen/Qwen3.8-27B ===", flush=True)
try:
    payload = {
        "model": "Qwen/Qwen3.8-27B",
        "messages": [
            {
                "role": "system",
                "content": "Eres el copiloto de Relationship Intelligence de Radar Comercial. Diseñas aperturas B2B directas y profesionales."
            },
            {
                "role": "user",
                "content": "Redacta un mensaje directo de LinkedIn (máximo 45 palabras) para contactar a Santiago Morales (VP de Pagos en Starpago) mencionando que ambos conocemos el ecosistema adquirente en México y proponiendo una charla de 10 min sobre optimización de tasas de aceptación."
            }
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    r_chat = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=15)
    print(f"Chat Status: {r_chat.status_code}", flush=True)
    if r_chat.status_code == 200:
        content = r_chat.json()['choices'][0]['message']['content']
        print(f"🎉 SUCCESS QWEN 3.8-27B:\n{content.strip()}", flush=True)
    else:
        print(f"Chat Error: {r_chat.text}", flush=True)
except Exception as e:
    print(f"Err chat: {e}", flush=True)

# 3. Test Qwen3-Embedding-8B
print("\n=== 3. PROBANDO EMBEDDINGS CON Qwen3-Embedding-8B ===", flush=True)
try:
    emb_payload = {
        "model": "Qwen3-Embedding-8B",
        "input": "VP de Operaciones y Medios de Pago en Fintech"
    }
    r_emb = requests.post(f"{base_url}/embeddings", headers=headers, json=emb_payload, timeout=10)
    print(f"Embedding Status: {r_emb.status_code}", flush=True)
    if r_emb.status_code == 200:
        emb_data = r_emb.json()['data'][0]['embedding']
        print(f"🎉 SUCCESS EMBEDDINGS! Vector dim: {len(emb_data)}", flush=True)
    else:
        print(f"Embedding Error: {r_emb.text}", flush=True)
except Exception as e:
    print(f"Err embedding: {e}", flush=True)
