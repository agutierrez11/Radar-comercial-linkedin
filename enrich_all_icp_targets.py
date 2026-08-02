import os
import csv
import json
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
enriched_json = os.path.join(os.path.dirname(__file__), "enriched_connections.json")

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
    print("🚀 === INICIANDO ENRIQUECIMIENTO COMPLETO DE LOS 69 CONTACTOS ICP PAYMENTS & C-LEVEL ===")
    
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN no encontrado en .env")
        return
        
    with open(enriched_json, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    terms = ['pay', 'pago', 'fintech', 'bank', 'banco', 'sales', 'ventas', 'growth', 'commercial', 'comercial', 'card', 'tarjeta', 'pos', 'acquiring', 'adquirencia', 'ceo', 'founder', 'fundador', 'director', 'vp', 'head', 'lead', 'owner', 'partner', 'e-commerce', 'ecommerce', 'retail']

    target_contacts = []
    for c in master_data:
        pos = (c.get('position') or '').lower()
        comp = (c.get('company') or '').lower()
        url = c.get('url') or ''
        full = f"{pos} {comp}"
        if url and any(t in full for t in terms):
            target_contacts.append(c)

    print(f"[+] Total de contactos ICP identificados a auditar: {len(target_contacts)}")
    target_urls = [c['url'] for c in target_contacts]
    
    actor_id = "harvestapi~linkedin-profile-posts"
    BATCH_SIZE = 10
    
    all_results = {}
    
    for i in range(0, len(target_urls), BATCH_SIZE):
        batch = target_urls[i:i+BATCH_SIZE]
        print(f"\n[...] Enviando lote {i//BATCH_SIZE + 1} de {len(target_urls)//BATCH_SIZE + 1} ({len(batch)} perfiles) a Apify...")
        
        payload = {
            "targetUrls": batch,
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
        
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                res_body = response.read().decode("utf-8")
                items = json.loads(res_body)
                print(f"  [+] Se recibieron {len(items)} ítems/posts para este lote.")
                
                for item in items:
                    if not item or not isinstance(item, dict):
                        continue
                    q = item.get("query", {})
                    t_url = q.get("targetUrl")
                    if t_url:
                        clean_t = t_url.strip().lower().split('?')[0].rstrip('/')
                        if clean_t not in all_results:
                            all_results[clean_t] = []
                        all_results[clean_t].append(item)
        except Exception as e:
            print(f"  [!] Error en lote {i//BATCH_SIZE + 1}: {e}")

    # Actualizar la Base de Datos Maestra Persistente
    updated_count = 0
    for c in master_data:
        c_url = (c.get("url") or "").strip().lower().split('?')[0].rstrip('/')
        if c_url in all_results:
            posts = all_results[c_url]
            if posts:
                p0 = posts[0]
                posted_at = p0.get("postedAt", {})
                c["audit_status"] = "Activo"
                c["last_post_date"] = posted_at.get("date", "Reciente")
                c["last_post_text"] = p0.get("content") or "Publicación multimedia/compartida"
                c["last_updated_apify"] = "2026-08-01"
                author_info = p0.get("author", {})
                if author_info.get("info"):
                    c["position"] = author_info.get("info")
            else:
                c["audit_status"] = "Inactivo/Sin Posts"
                c["last_post_date"] = "Sin publicaciones recientes"
                c["last_post_text"] = "No se encontraron publicaciones públicas"
                c["last_updated_apify"] = "2026-08-01"
            updated_count += 1

    with open(enriched_json, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ ¡ENRIQUECIMIENTO ICP MASIVO FINALIZADO! Se actualizaron {updated_count} perfiles en 'enriched_connections.json'.")

if __name__ == "__main__":
    main()
