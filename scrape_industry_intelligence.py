import os
import json
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
industry_intel_file = os.path.join(os.path.dirname(__file__), "starpago_industry_intelligence.json")

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

TARGET_PAGES = [
    "https://www.linkedin.com/company/nuvei",
    "https://www.linkedin.com/company/unlimit",
    "https://www.linkedin.com/company/nium",
    "https://www.linkedin.com/company/dlocal",
    "https://www.linkedin.com/company/rapyd",
    "https://www.linkedin.com/company/ebanx",
    "https://www.linkedin.com/company/airwallex",
    "https://www.linkedin.com/company/stripe",
    "https://www.linkedin.com/company/fintoc",
    "https://www.linkedin.com/company/kasnet"
]

def main():
    print("🚀 === EXTRACCIÓN BATCH POR PARTES (INTELIGENCIA DE COMPETENCIA & INDUSTRIA) ===")
    
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN no encontrado en .env")
        return

    actor_id = "harvestapi~linkedin-profile-posts"
    BATCH_SIZE = 2  # Procesar de 2 en 2 para evitar timeouts HTTP
    
    all_news = []
    
    for i in range(0, len(TARGET_PAGES), BATCH_SIZE):
        batch = TARGET_PAGES[i:i+BATCH_SIZE]
        print(f"\n[...] Procesando lote industria {i//BATCH_SIZE + 1} ({len(batch)} empresas)...")
        for u in batch:
            print(f"  • {u}")
            
        payload = {
            "targetUrls": batch,
            "maxPosts": 3,
            "scrapeComments": False,
            "scrapeReactions": True
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        url_api = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
        
        req = urllib.request.Request(
            url_api,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                res_body = response.read().decode("utf-8")
                items = json.loads(res_body)
                print(f"    [+] Recibidos {len(items)} posts/noticias.")
                
                for item in items:
                    if not item or not isinstance(item, dict):
                        continue
                    content = item.get("content") or ""
                    posted_at = (item.get("postedAt") or {}).get("date", "")
                    author = (item.get("author") or {}).get("name", "Empresa Competidora")
                    likes = (item.get("engagement") or {}).get("likes", 0)
                    url_post = item.get("linkedinUrl") or ""
                    
                    if content:
                        all_news.append({
                            "company": author,
                            "date": posted_at,
                            "content": content,
                            "likes": likes,
                            "url": url_post
                        })
        except Exception as e:
            print(f"    [!] Error en lote: {e}")
            
    final_output = {
        "total_posts": len(all_news),
        "news": all_news
    }
    
    with open(industry_intel_file, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ ¡INTELIGENCIA DE INDUSTRIA COMPLETADA Y GUARDADA! ({len(all_news)} publicaciones/noticias extraídas).")

if __name__ == "__main__":
    main()
