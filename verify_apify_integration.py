import os
import json
import urllib.request
import urllib.error
import sys

# Configurar consola en UTF-8 para evitar errores de impresión en Windows
sys.stdout.reconfigure(encoding='utf-8')

def load_env():
    """Reads local .env file without external dependencies."""
    env = {}
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def main():
    print("=== PRUEBA DE INTEGRACIÓN CON APIFY ===")
    
    # 1. Cargar variables
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    
    if not token or token == "tu_key_de_apify_aqui" or token == "":
        print("\n[!] ERROR: APIFY_API_TOKEN no configurado en el archivo .env.")
        print("Asegúrate de haber guardado tu API Key en el archivo .env antes de correr esta prueba.")
        return
        
    # 2. Configurar perfil de prueba
    # Usaremos una URL de perfil de prueba de tus conexiones
    test_profile = "https://www.linkedin.com/in/rahulnaidu9"
    print(f"\nPerfil de prueba seleccionado: {test_profile}")
    
    # 3. Configurar payload de entrada para linkedin-profile-scraper
    payload = {
        "urls": [test_profile],
        "minDelay": 1,
        "maxDelay": 5
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    
    # Usamos harvestapi~linkedin-profile-scraper
    actor_id = "harvestapi~linkedin-profile-scraper"
    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    print("Enviando petición a la API de Apify (ejecutando actor síncrono)...")
    print("Esto puede tomar de 1 a 3 minutos ya que Apify levanta un navegador en la nube.")
    
    try:
        # Petición HTTP síncrona
        with urllib.request.urlopen(req, timeout=300) as response:
            res_body = response.read().decode("utf-8")
            items = json.loads(res_body)
            
            print(f"\n[+] ÉXITO: Petición respondida por Apify. Se obtuvieron {len(items)} registros.")
            print("\nRESULTADOS DE PERFILES:")
            
            if not items:
                print("No se encontraron datos para este perfil.")
            else:
                profile = items[0]
                print("\nEstructura de datos devuelta por el scraper (Muestra):")
                
                print(f"Name: {profile.get('firstName')} {profile.get('lastName')}")
                print(f"Headline: {profile.get('headline')}")
                loc = profile.get('location', {})
                print(f"Location: {loc.get('linkedinText', 'Desconocido') if isinstance(loc, dict) else loc}")
                
                # Intentamos extraer industria de la experiencia actual si no está a nivel raíz
                industry = profile.get('industry')
                if not industry and profile.get('experience'):
                    # A veces la industria está implícita o podemos tomar la empresa actual
                    industry = profile['experience'][0].get('companyName')
                print(f"Industry (or Current Company): {industry}")
                
                # Save raw json for debug
                with open('verify_apify_raw.json', 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2, ensure_ascii=False)
                print("\nJSON crudo guardado en 'verify_apify_raw.json'")
            
    except urllib.error.HTTPError as e:
        print(f"\n[!] ERROR HTTP de Apify (Código {e.code}):")
        try:
            error_details = e.read().decode("utf-8")
            print(f"Detalles: {error_details}")
        except Exception:
            print(f"Mensaje de error: {e.reason}")
    except urllib.error.URLError as e:
        print(f"\n[!] ERROR de Red / Conexión: {e.reason}")
    except Exception as e:
        print(f"\n[!] ERROR Inesperado: {e}")

if __name__ == "__main__":
    main()
