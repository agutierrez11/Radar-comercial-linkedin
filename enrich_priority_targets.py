import os
import csv
import json
import urllib.request
import urllib.error
import sys

# Configurar UTF-8 en consola Windows
sys.stdout.reconfigure(encoding='utf-8')

# Archivos de trabajo
env_path = os.path.join(os.path.dirname(__file__), ".env")
connections_file = os.path.join(os.path.dirname(__file__), "Connections.csv")
enriched_json = os.path.join(os.path.dirname(__file__), "enriched_connections.json")
progress_file = os.path.join(os.path.dirname(__file__), "enrichment_progress.json")

# Lista prioritaria de las 5 perfiles estratégicos elegidos para Starpago:
PRIORITY_URLS = [
    "https://www.linkedin.com/in/lezorich",                 # Lukas Zorich (Fintoc)
    "https://www.linkedin.com/in/rdz-igor-alex",            # Alejandro Rodríguez (Affipay / Mi Banco Autofin)
    "https://www.linkedin.com/in/annick-olim%C3%B3n-vivot", # Annick Olimón Vivot (Uber Eats LatAm)
    "https://www.linkedin.com/in/guillermoaraujo",          # Guillermo Araujo (TEKSOL)
    "https://www.linkedin.com/in/selena-serv%C3%ADn-ventifyl" # Selena Servín (Ventify)
]

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

def main():
    print("🚀 === INICIANDO ENRIQUECIMIENTO MAESTRO PERSISTENTE (STARPAGO TARGETS) ===")
    
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN no encontrado en .env")
        return
        
    print(f"\n[+] Se enriquecerán y actualizarán los siguientes 5 decisores prioritarios:")
    for url in PRIORITY_URLS:
        print(f"  • {url}")
        
    actor_id = "harvestapi~linkedin-profile-posts"
    
    payload = {
        "targetUrls": PRIORITY_URLS,
        "maxPosts": 3,
        "scrapeComments": False,
        "scrapeReactions": False
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    url_api = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
    
    req = urllib.request.Request(
        url_api,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    print("\n[...] Solicitando auditoría y datos frescos a Apify (esto toma ~1 minuto)...")
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            res_body = response.read().decode("utf-8")
            items = json.loads(res_body)
            print(f"[+] Éxito: Se recibieron {len(items)} ítems/publicaciones desde Apify.")
            
            # Organizar resultados por URL limpia
            results_by_url = {}
            for url in PRIORITY_URLS:
                clean_u = url.strip().lower().split('?')[0].rstrip('/')
                results_by_url[clean_u] = []
                
            for item in items:
                if not item or not isinstance(item, dict):
                    continue
                q = item.get("query", {})
                target_url = q.get("targetUrl")
                if target_url:
                    target_clean = target_url.strip().lower().split('?')[0].rstrip('/')
                    for u_key in results_by_url:
                        if u_key in target_clean or target_clean in u_key:
                            results_by_url[u_key].append(item)
                            
            # Cargar dataset local enriched_connections.json para fusionar
            if os.path.exists(enriched_json):
                with open(enriched_json, "r", encoding="utf-8") as f:
                    master_data = json.load(f)
            else:
                master_data = []
                
            print("\n📊 === RESULTADOS DEL ENRIQUECIMIENTO ===")
            updated_count = 0
            
            for url in PRIORITY_URLS:
                clean_u = url.strip().lower().split('?')[0].rstrip('/')
                posts = results_by_url.get(clean_u, [])
                
                # Buscar en master_data
                contact_entry = None
                for c in master_data:
                    c_u = c.get("url", "").strip().lower().split('?')[0].rstrip('/')
                    if c_u and (c_u in clean_u or clean_u in c_u):
                        contact_entry = c
                        break
                        
                last_post_date = "Sin publicaciones recientes"
                last_post_text = "No se encontraron posts activos"
                author_info = {}
                
                if posts:
                    p0 = posts[0]
                    posted_at = p0.get("postedAt", {})
                    last_post_date = posted_at.get("date", "Reciente")
                    last_post_text = p0.get("content") or "Publicación multimedia/compartida"
                    author_info = p0.get("author", {})
                    
                print(f"\n👤 Perfil: {clean_u}")
                print(f"   • Última Publicación: {last_post_date}")
                print(f"   • Extracto Post: {last_post_text[:120]}...")
                
                if contact_entry:
                    contact_entry["audit_status"] = "Activo"
                    contact_entry["last_post_date"] = last_post_date
                    contact_entry["last_post_text"] = last_post_text
                    contact_entry["last_updated_apify"] = "2026-08-01"
                    if author_info.get("info"):
                        contact_entry["position"] = author_info.get("info")
                    updated_count += 1
                    
            # Guardar la Base de Datos Maestra Enriquecida
            with open(enriched_json, "w", encoding="utf-8") as f:
                json.dump(master_data, f, indent=2, ensure_ascii=False)
                
            print(f"\n✅ ¡PROCESO COMPLETADO! Se actualizaron {updated_count} perfiles en 'enriched_connections.json'.")
            print("💾 Los datos actualizados han quedado guardados en la Base de Datos Maestra Persistente.")

    except Exception as e:
        print(f"[!] Error ejecutando Apify: {e}")

if __name__ == "__main__":
    main()
