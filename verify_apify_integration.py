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
    
    # 3. Configurar payload de entrada
    payload = {
        "targetUrls": [test_profile],
        "maxPosts": 3,
        "scrapeComments": False,
        "scrapeReactions": False
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    
    # Usamos la ejecución síncrona para que retorne los resultados directamente en una sola petición
    actor_id = "harvestapi~linkedin-profile-posts"
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
            print("\nRESULTADOS DE PUBLICACIONES:")
            
            if not items:
                print("No se encontraron publicaciones recientes para este perfil o el perfil está inactivo/privado.")
            else:
                # Imprimir el primer registro completo para inspeccionar su estructura real
                print("\nEstructura de datos devuelta por el scraper (Muestra del primer ítem):")
                print(json.dumps(items[0], indent=2, ensure_ascii=False))
                print("-" * 50)
                
                for idx, item in enumerate(items, 1):
                    if not item or not isinstance(item, dict):
                        continue
                        
                    # Extraer campos reales según la estructura de harvestapi
                    content_val = item.get("content")
                    text = str(content_val) if content_val else "Sin texto (Solo Multimedia o Compartido)"
                    
                    # Extraer fecha del objeto anidado postedAt
                    posted_at_obj = item.get("postedAt") or {}
                    post_date = posted_at_obj.get("date")
                    posted_ago = posted_at_obj.get("postedAgoText")
                    
                    if post_date and posted_ago:
                        date_display = f"{post_date} ({posted_ago})"
                    elif post_date:
                        date_display = post_date
                    elif posted_ago:
                        date_display = posted_ago
                    else:
                        date_display = "Fecha desconocida"
                    
                    # Enlace
                    post_url = item.get("linkedinUrl") or item.get("shareLinkedinUrl")
                    post_url = str(post_url) if post_url else "Sin URL"
                    
                    print(f"\n--- Post {idx} ---")
                    print(f"Fecha: {date_display}")
                    print(f"Enlace: {post_url}")
                    print(f"Texto: {text[:150].replace(chr(10), ' ')}...")


            
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
