import urllib.request
import json
import os
import sys

# Configurar stdout para usar UTF-8 en Windows y evitar errores de codificación
sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")

def load_env():
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def test_key(key, model):
    print(f"\nProbando con modelo '{model}'...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hola, responde únicamente con la palabra 'FUNCIONA' si recibes este mensaje correctamente."
            }]
        }]
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            text = res_json["candidates"][0]["content"]["parts"][0]["text"]
            print(f"  [✓] ¡ÉXITO! Respuesta de Gemini: '{text.strip()}'")
            return True
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
            err_json = json.loads(err_body)
            err_msg = err_json.get("error", {}).get("message", "Error HTTP desconocido")
            print(f"  [!] HTTP Error {e.code}: {err_msg}")
        except Exception:
            print(f"  [!] HTTP Error {e.code}")
        return False
    except Exception as e:
        print(f"  [!] Error de red: {e}")
        return False

def main():
    env = load_env()
    key = env.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY no encontrada en .env")
        return
        
    print(f"Iniciando prueba con la clave del .env: {key[:8]}...{key[-8:]}")
    
    models_to_test = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-3.5-flash",
        "gemini-pro-latest"
    ]
    
    success = False
    for model in models_to_test:
        if test_key(key, model):
            print(f"\n[✓] ¡CONEXIÓN EXITOSA con el modelo '{model}'!")
            success = True
            break
            
    if not success:
        print("\n[!] No se pudo conectar con ninguno de los modelos probados.")

if __name__ == "__main__":
    main()
