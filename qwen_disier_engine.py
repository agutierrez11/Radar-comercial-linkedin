import os
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DISIER_KEY = "sk-0MINhr9-vEmzYLUFx-OvjQ"
DISIER_BASE_URL = "https://llm.disier.net/v1"

def generar_prospeccion_qwen(
    nombre_prospecto: str,
    cargo: str,
    empresa: str,
    conexion_comun: str,
    propuesta_valor: str
) -> dict:
    """
    Invoca Qwen/Qwen3.8-27B en Disier y separa el Razonamiento Estratégico del Mensaje Final.
    """
    headers = {
        "Authorization": f"Bearer {DISIER_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Actúa como un estratega de ventas B2B y Relationship Intelligence de Radar Comercial.
Redacta un mensaje directo de LinkedIn (máximo 45 palabras, sin sonar a spam corporativo ni venta agresiva):
- Prospecto: {nombre_prospecto} ({cargo} en {empresa})
- Puente cálido / Contexto compartido: {conexion_comun}
- Propuesta de valor: {propuesta_valor}

Regla: Enfócate en abrir conversación o pedir una breve opinión sobre el desafío común."""

    payload = {
        "model": "Qwen/Qwen3.8-27B",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.6,
        "stream": True
    }

    try:
        r = requests.post(f"{DISIER_BASE_URL}/chat/completions", headers=headers, json=payload, stream=True, timeout=30)
        if r.status_code != 200:
            return {"success": False, "error": f"Status {r.status_code}: {r.text}"}

        reasoning = ""
        final_content = ""

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
                        # If the server sends reasoning_content separately
                        if "reasoning_content" in delta and delta["reasoning_content"]:
                            reasoning += delta["reasoning_content"]
                        elif "content" in delta and delta["content"]:
                            final_content += delta["content"]
                    except Exception:
                        pass

        # If reasoning and content were bundled in content
        if not reasoning and not final_content:
            return {"success": False, "error": "Respuesta vacía"}

        return {
            "success": True,
            "model": "Qwen/Qwen3.8-27B (Disier)",
            "razonamiento_estrategico": reasoning.strip(),
            "mensaje_final": final_content.strip()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    res = generar_prospeccion_qwen(
        nombre_prospecto="Santiago Morales",
        cargo="VP de Operaciones y Medios de Pago",
        empresa="Starpago Latam",
        conexion_comun="Ambos coincidieron en el ecosistema adquirente de México",
        propuesta_valor="Minería de relaciones de 1er grado para acelerar cierres enterprise"
    )
    print("=== RESPUESTA DE QWEN 3.8 ===", flush=True)
    print(f"Success: {res.get('success')}", flush=True)
    print(f"Modelo: {res.get('model')}", flush=True)
    if res.get("razonamiento_estrategico"):
        print("\n🧠 [RAZONAMIENTO ESTRATÉGICO / THINKING TRACE]:")
        print(res["razonamiento_estrategico"][:300] + "...")
    print("\n📩 [MENSAJE DE LINKEDIN LISTO]:")
    print(res.get("mensaje_final"))
