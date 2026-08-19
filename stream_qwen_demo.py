import os
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DISIER_KEY = "sk-0MINhr9-vEmzYLUFx-OvjQ"
DISIER_BASE_URL = "https://llm.disier.net/v1"

def stream_prospeccion_qwen(
    nombre_prospecto: str,
    cargo: str,
    empresa: str,
    conexion_comun: str,
    propuesta_valor: str
):
    headers = {
        "Authorization": f"Bearer {DISIER_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Actúa como un estratega comercial B2B de Radar Comercial.
Redacta un mensaje directo de LinkedIn (máximo 45 palabras, sin rodeos ni venta agresiva):
- Prospecto: {nombre_prospecto} ({cargo} en {empresa})
- Puente cálido / Contexto compartido: {conexion_comun}
- Propuesta de valor: {propuesta_valor}

Regla: Enfócate en abrir conversación o pedir una breve opinión sobre el desafío común."""

    payload = {
        "model": "Qwen/Qwen3.8-27B",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.6,
        "stream": True
    }

    print("🚀 Conectando con Qwen 3.8 (27B) en Disier...\n", flush=True)
    
    r = requests.post(f"{DISIER_BASE_URL}/chat/completions", headers=headers, json=payload, stream=True, timeout=60)
    
    in_reasoning = False
    in_content = False
    
    for line in r.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                data_str = decoded[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk['choices'][0].get('delta', {})
                    
                    # Manejo de Thinking Trace (Razonamiento)
                    reasoning_chunk = delta.get('reasoning_content')
                    if reasoning_chunk:
                        if not in_reasoning:
                            print("🧠 [PENSAMIENTO ESTRATÉGICO / REASONING]:\n", flush=True)
                            in_reasoning = True
                        print(reasoning_chunk, end="", flush=True)
                    
                    # Manejo del Mensaje Final
                    content_chunk = delta.get('content')
                    if content_chunk:
                        if not in_content:
                            print("\n\n" + "="*50, flush=True)
                            print("📩 [MENSAJE FINAL DE LINKEDIN]:\n", flush=True)
                            in_content = True
                        print(content_chunk, end="", flush=True)
                except Exception:
                    pass
    print("\n" + "="*50, flush=True)

if __name__ == "__main__":
    stream_prospeccion_qwen(
        nombre_prospecto="Santiago Morales",
        cargo="VP de Operaciones y Medios de Pago",
        empresa="Starpago Latam",
        conexion_comun="Ambos coincidieron en el ecosistema adquirente de México",
        propuesta_valor="Minería de relaciones de 1er grado para acelerar cierres enterprise"
    )
