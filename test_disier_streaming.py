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

payload = {
    "model": "Qwen/Qwen3.8-27B",
    "messages": [
        {"role": "user", "content": "Di exactamente: 'Qwen 3.8 conectado y listo para la demo'"}
    ],
    "max_tokens": 150,
    "stream": True
}

print("=== INICIANDO PRUEBA STREAMING CON QWEN 3.8 ===", flush=True)

try:
    r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, stream=True, timeout=30)
    print(f"Status Code: {r.status_code}", flush=True)
    full_text = ""
    for line in r.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                data_str = decoded[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk['choices'][0].get('delta', {})
                    content = delta.get('content') or delta.get('reasoning_content') or ""
                    full_text += content
                    print(content, end="", flush=True)
                except Exception:
                    pass
    print("\n\n=== TEXTO COMPLETO GENERADO ===", flush=True)
    print(full_text, flush=True)
except Exception as e:
    print(f"Error en streaming: {e}", flush=True)
