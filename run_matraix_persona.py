import yaml
import json
import glob
import os
import google.generativeai as genai

# Setup Gemini API key
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_KEY:
    # Try finding in .env
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    GEMINI_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def load_persona(persona_id_or_path):
    if os.path.exists(persona_id_or_path):
        filepath = persona_id_or_path
    else:
        filepath = f"scratch/MatrAIx-Persona-8B/persona/datasets/matraix-persona-dev-sample/persona_{persona_id_or_path}.yaml"
        if not os.path.exists(filepath):
            files = glob.glob("scratch/MatrAIx-Persona-8B/persona/datasets/matraix-persona-dev-sample/*.yaml")
            filepath = files[0] if files else ""

    if not filepath or not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_persona_simulation(persona_data, user_pitch):
    dims = persona_data.get('dimensions', {})
    name = persona_data.get('display_name', 'Buyer Persona')
    
    system_instruction = f"""
Eres {name}, un prospecto comercial real simulado por el framework MatrAIx-Persona-8B.
Tus dimensiones psicológicas y profesionales son:
- Cargo/Función: {dims.get('role_function', 'Director')} en {dims.get('domain', 'Business')} ({dims.get('seniority', 'Senior')} seniority)
- Tamaño de empresa: {dims.get('company_size', 'Mid-market')}
- Nivel de experiencia: {dims.get('years_experience', '10+')} años
- Estilo de decisión: {dims.get('decision_style', 'Analítico/Directivo')}
- Tolerancia al riesgo: {dims.get('risk_tolerance', 'Alta aversión al riesgo / Conservador')}
- Nivel tecnológico: {dims.get('tech_savviness', 'Pragmático')}
- Prioridades: {dims.get('values_priority', 'Eficiencia, ROI y Seguridad de datos')}

REGLAS DE ACTUACIÓN (MatrAIx Simulation Rules):
1. NO seas complaciente ni amable por defecto. Actúa como un decisor corporativo ocupado.
2. Si la propuesta de venta suena a spam o carece de ROI claro, cuestiona duramente, pon objeciones de presupuesto o tiempo.
3. Evalúa si el pitch conecta con tus dolores de negocio.
4. Responde en español directo en 2-4 oraciones desde tu personaje.
"""

    if not GEMINI_KEY:
        return f"[{name} - Simulación Local Sin API Key]\n'Tu pitch me parece interesante pero no veo claro el ROI para mi empresa. ¿Qué garantía de datos me das y cuánto cuesta en comparación con soluciones existentes?'"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"INSTRUCCIONES DE SISTEMA:\n{system_instruction}\n\nEL VENDEDOR DICE:\n\"{user_pitch}\"\n\nTU RESPUESTA COMO {name}:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al simular persona con Gemini API: {e}"

if __name__ == "__main__":
    p = load_persona("0145")
    if p:
        print(f"Loaded Persona: {p.get('display_name')}")
        pitch = "Hola, vi que estás optimizando los procesos comerciales de tu equipo. Desarrollamos Radar Comercial, un sistema agéntico 100% local que actualiza los cargos de tus contactos de LinkedIn y detecta intenciones de compra con IA sin servidor."
        reply = run_persona_simulation(p, pitch)
        print("\n--- SIMULACIÓN DE RESPUESTA ---")
        print(reply)
