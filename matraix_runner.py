import os
import json
import yaml
import glob
import urllib.request
import urllib.parse
import sys

# Extract GEMINI_API_KEY from env or .env file
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_KEY and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

def load_persona(persona_id="0145"):
    # Path inside cloned MatrAIx repo
    base_dir = "scratch/MatrAIx-Persona-8B/persona/datasets/matraix-persona-dev-sample"
    filepath = os.path.join(base_dir, f"persona_{persona_id}.yaml")
    
    if not os.path.exists(filepath):
        # Fallback to any yaml file in dev-sample
        files = glob.glob(os.path.join(base_dir, "*.yaml"))
        if files:
            filepath = files[0]

    if not os.path.exists(filepath):
        print(f"Error: Persona file not found in {base_dir}")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_simulation(persona_data, user_pitch):
    dims = persona_data.get('dimensions', {})
    name = persona_data.get('display_name', 'Simulated Persona')
    
    system_prompt = f"""
[MatrAIx-Persona-8B Simulation Context]
Persona ID: {persona_data.get('persona_id')}
Nombre: {name}
Cargo / Dominio: {dims.get('role_function', 'Director')} en {dims.get('domain', 'Negocios')}
Seniority: {dims.get('seniority', 'Senior')} ({dims.get('years_experience', '5+')} años de exp)
Tamaño de Empresa: {dims.get('company_size', 'Mid-Market / Enterprise')}
Tolerancia al Riesgo: {dims.get('risk_tolerance', 'Averso al Riesgo / Conservador')}
Estilo de Decisión: {dims.get('decision_style', 'Analítico / Directivo')}
Prioridades de Valor: {dims.get('values_priority', 'ROI Claro, Seguridad y Eficiencia')}
Rasgo Dominante: {dims.get('dominant_trait', 'Exigente / Pragmático')}

REGLAS DE SIMULACIÓN MATRAIX:
1. Actúa 100% como {name}. NO seas complaciente ni amable por defecto.
2. Si el mensaje de venta suena a spam o buzzwords vacíos ("IA agéntica", "revolucionario"), cuestiona duramente el costo, el tiempo de implementación y la seguridad.
3. Expresa objeciones reales de negocio según tu nivel de seniority y prioridades.
4. Responde en español directo en 2-4 oraciones.
"""

    if not GEMINI_KEY:
        print("Warning: GEMINI_API_KEY not found. Running simulated offline fallback.")
        return f"[{name} - Modo Offline]\n'Me parece interesante pero necesito ver métricas claras de ROI y garantías de privacidad antes de evaluar cualquier software.'"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{system_prompt}\n\nVENDEDOR DICE: \"{user_pitch}\"\n\nTU RESPUESTA COMO {name}:"
            }]
        }]
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            res_json = json.loads(resp.read().decode('utf-8'))
            text = res_json['candidates'][0]['content']['parts'][0]['text']
            return text.strip()
    except Exception as e:
        return f"Error en la llamada REST a Gemini API: {e}"

if __name__ == "__main__":
    persona_id = sys.argv[1] if len(sys.argv) > 1 else "0145"
    pitch = sys.argv[2] if len(sys.argv) > 2 else "Hola, desarrollamos Radar Comercial para actualizar automaticamente el cargo de tus contactos de LinkedIn y detectar oportunidades de venta calidas sin enviar spam."
    
    p = load_persona(persona_id)
    if p:
        dims = p.get('dimensions', {})
        print("============================================================")
        print("MATRAIX PERSONA SIMULATION ENGINE")
        print(f"   Persona: {p.get('display_name')} (ID: {p.get('persona_id')})")
        print(f"   Cargo: {dims.get('role_function')} | Dominio: {dims.get('domain')}")
        print(f"   Decision: {dims.get('decision_style')} | Riesgo: {dims.get('risk_tolerance')}")
        print("============================================================")
        print(f"\nPITCH ENTRANTE:\n\"{pitch}\"\n")
        print("RESPUESTA SIMULADA POR MATRAIX:")
        reply = run_simulation(p, pitch)
        print(f"{reply}")
        print("============================================================\n")
