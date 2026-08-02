import os
import json
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
intel_output_file = os.path.join(os.path.dirname(__file__), "target_intel_posts.json")

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

def fetch_target_intelligence(target_urls):
    """
    Función exclusiva para Inteligencia Comercial:
    Solo extrae publicaciones profundas de competidores o clientes objetivos seleccionados.
    """
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN no encontrado en .env")
        return []

    actor_id = "harvestapi~linkedin-profile-posts"
    payload = {
        "targetUrls": target_urls,
        "maxPosts": 3,
        "scrapeComments": True,
        "scrapeReactions": True
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    url_api = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
    
    req = urllib.request.Request(
        url_api,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"🕵️‍♂️ [INTELIGENCIA COMERCIAL] Solicitando scraping profundo para {len(target_urls)} perfiles objetivo/competidores...")
    
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            res_body = response.read().decode("utf-8")
            items = json.loads(res_body)
            print(f"[+] Éxito: Obtenidos {len(items)} posts/comentarios para inteligencia comercial.")
            
            with open(intel_output_file, "w", encoding="utf-8") as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
                
            return items
    except Exception as e:
        print(f"[!] Error extrayendo inteligencia comercial: {e}")
        return []

if __name__ == "__main__":
    # Ejemplo de uso bajo demanda: solo la competencia y clientes VIP elegidos por Antonio
    test_targets = [
        "https://www.linkedin.com/in/martinaselser", # VP Growth @ Unlimit
        "https://www.linkedin.com/in/anroldan"        # Sr Sales Manager iGaming @ Nuvei
    ]
    fetch_target_intelligence(test_targets)
