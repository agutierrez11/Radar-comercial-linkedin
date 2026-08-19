import os
import requests
import json
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

DISIER_KEY = os.getenv("DISIER_API_KEY", "sk-0MINhr9-vEmzYLUFx-OvjQ")
DISIER_BASE_URL = os.getenv("DISIER_BASE_URL", "https://llm.disier.net/v1")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def generar_prospeccion_b2b(
    nombre_prospecto: str,
    cargo: str,
    empresa: str,
    conexion_comun: str,
    propuesta_valor: str,
    mostrar_pensamiento: bool = False
) -> dict:
    """
    Motor Híbrido de Prospección de Radar Comercial:
    1. Intenta invocar Qwen/Qwen3.8-27B (Disier) con soporte de Thinking/Reasoning.
    2. Si hay timeout o error, salta a Google Gemini 2.5 Flash de forma transparente.
    """
    prompt = f"""Actúa como el copiloto comercial de Radar Comercial.
Redacta un mensaje directo de LinkedIn (máximo 45 palabras, profesional, sin rodeos ni venta agresiva):
- Prospecto: {nombre_prospecto} ({cargo} en {empresa})
- Puente cálido / Contexto compartido: {conexion_comun}
- Propuesta de valor: {propuesta_valor}

Regla: Enfócate en abrir una conversación de valor o pedir su opinión técnica/comercial."""

    # 1. Intentar con Qwen 3.8-27B (Disier)
    if DISIER_KEY:
        try:
            payload = {
                "model": "Qwen/Qwen3.8-27B",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2500,
                "temperature": 0.6,
                "stream": True
            }
            r = requests.post(
                f"{DISIER_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {DISIER_KEY}", "Content-Type": "application/json"},
                json=payload,
                stream=True,
                timeout=40
            )
            if r.status_code == 200:
                reasoning = ""
                content = ""
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
                                if "reasoning_content" in delta and delta["reasoning_content"]:
                                    reasoning += delta["reasoning_content"]
                                if "content" in delta and delta["content"]:
                                    content += delta["content"]
                            except Exception:
                                pass
                
                if content.strip():
                    return {
                        "success": True,
                        "provider": "Qwen/Qwen3.8-27B (Disier AI)",
                        "razonamiento": reasoning.strip() if mostrar_pensamiento else None,
                        "mensaje": content.strip()
                    }
        except Exception:
            pass

    # 2. Fallback Seguro: Google Gemini 2.5 Flash
    if GEMINI_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 300, "temperature": 0.7}
            }
            r = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=8)
            if r.status_code == 200:
                res_data = r.json()
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "success": True,
                    "provider": "Google Gemini 2.5 Flash (Fallback)",
                    "razonamiento": None,
                    "mensaje": text.strip()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "No hay proveedor LLM disponible."}

if __name__ == "__main__":
    print("=== MOTOR DE PROSPECCIÓN RADAR COMERCIAL ===", flush=True)
    res = generar_prospeccion_b2b(
        nombre_prospecto="Santiago Morales",
        cargo="VP de Operaciones y Medios de Pago",
        empresa="Starpago Latam",
        conexion_comun="Ambos coincidieron en el ecosistema adquirente de México",
        propuesta_valor="Minería de relaciones de 1er grado para acelerar cierres enterprise",
        mostrar_pensamiento=True
    )
    print(f"Estado: {'✅ Operativo' if res.get('success') else '❌ Falló'}", flush=True)
    print(f"Proveedor Activo: {res.get('provider')}", flush=True)
    if res.get("razonamiento"):
        print("\n🧠 Pensamiento del Modelo:", flush=True)
        print(res["razonamiento"][:250] + "...\n", flush=True)
    print("📩 Mensaje Generado:", flush=True)
    print(res.get("mensaje"), flush=True)
