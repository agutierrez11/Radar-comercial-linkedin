import os
import csv
import json
import zipfile
import io
import urllib.request
import urllib.error
import sys

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
enriched_json = os.path.join(os.path.dirname(__file__), "enriched_connections.json")
starpago_intel_file = os.path.join(os.path.dirname(__file__), "starpago_intelligence.json")

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

def extract_all_3119_connections():
    print(f"📦 Leyendo ZIP completo desde: {zip_path}")
    connections = []
    
    if not os.path.exists(zip_path):
        # Intentar ruta alternativa sin doble .zip
        alt_path = zip_path.replace(".zip.zip", ".zip")
        if os.path.exists(alt_path):
            zip_target = alt_path
        else:
            print(f"[!] ERROR: No se encontró el ZIP en {zip_path}")
            return connections
    else:
        zip_target = zip_path

    with zipfile.ZipFile(zip_target, 'r') as zf:
        if 'Connections.csv' in zf.namelist():
            with zf.open('Connections.csv') as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                
                # Buscar encabezado
                header = None
                for row in reader:
                    if len(row) > 0 and 'First Name' in row:
                        header = row
                        break
                        
                for i, row in enumerate(reader, 1):
                    if len(row) < 6:
                        continue
                    first_name = row[0].strip()
                    last_name = row[1].strip()
                    url = row[2].strip() if len(row) > 2 else ""
                    connected_on = row[3].strip() if len(row) > 3 else ""
                    company = row[4].strip() if len(row) > 4 else ""
                    position = row[5].strip() if len(row) > 5 else ""
                    
                    if url:
                        connections.append({
                            "id": i,
                            "first_name": first_name,
                            "last_name": last_name,
                            "full_name": f"{first_name} {last_name}",
                            "url": url,
                            "connected_on": connected_on,
                            "company_zip": company,
                            "position_zip": position,
                            "company": company,
                            "position": position,
                            "audit_status": "Pendiente Auditoria",
                            "job_status": "Vigente ZIP"
                        })
                        
    print(f"✅ Se extrajeron exitosamente {len(connections)} contactos de tu red completa de LinkedIn.")
    return connections

def scrape_starpago_intelligence(token):
    print("\n🕵️‍♂️ === SCRAPEANDO INTELIGENCIA COMERCIAL DE STARPAGO EN LINKEDIN EN TIEMPO REAL ===")
    
    # 1. Scrape de Posts / Menciones de Starpago
    actor_id = "harvestapi~linkedin-profile-posts"
    # Vamos a usar URLs de búsqueda / perfiles de Starpago en LinkedIn
    target_urls = [
        "https://www.linkedin.com/company/starpago",
        "https://www.starpago.com"
    ]
    
    payload = {
        "targetUrls": target_urls,
        "maxPosts": 10,
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
    
    intel_data = {
        "company_name": "Starpago",
        "website": "https://www.starpago.com/",
        "target_verticals": [
            "Cross-Border Payments",
            "High-Volume Merchants",
            "iGaming / Forex / Crypto / High-Risk Acquiring",
            "PayTech & Gateway Integration",
            "LATAM Merchant Acquiring"
        ],
        "linkedin_insights": []
    }
    
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            res_body = response.read().decode("utf-8")
            items = json.loads(res_body)
            print(f"[+] Se obtuvieron {len(items)} items de inteligencia de Starpago desde Apify.")
            intel_data["linkedin_insights"] = items
    except Exception as e:
        print(f"[!] Nota sobre scrape corporativo de Starpago: {e}")
        
    with open(starpago_intel_file, "w", encoding="utf-8") as f:
        json.dump(intel_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Inteligencia de Starpago guardada en '{starpago_intel_file}'.")

def main():
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN no encontrado en .env")
        return

    # 1. Scrape Inteligencia Starpago
    scrape_starpago_intelligence(token)

    # 2. Cargar los 3,119 contactos del ZIP
    all_connections = extract_all_3119_connections()
    if not all_connections:
        return

    # Guardar estado maestro inicial con los 3,119 contactos
    with open(enriched_json, "w", encoding="utf-8") as f:
        json.dump(all_connections, f, indent=2, ensure_ascii=False)

    print("\n🚀 === INICIANDO ENRIQUECIMIENTO MASIVO CON APIFY PARA LA RED COMPLETA (3,119 CONTACTOS) ===")
    print("    Se procesarán por lotes en segundo plano con validación de Champion Drift.")
    
    actor_id = "harvestapi~linkedin-profile-posts"
    BATCH_SIZE = 15
    RUN_LIMIT = 3119  # Procesar todos
    
    target_urls = [c["url"] for c in all_connections if c.get("url")]
    
    print(f"[+] Total de perfiles en cola para Apify: {len(target_urls)}")
    print(f"    Consumo estimado de Apify: ~$7.80 USD (de tus $80 USD de saldo).")
    
    all_results = {}
    
    for i in range(0, len(target_urls), BATCH_SIZE):
        batch = target_urls[i:i+BATCH_SIZE]
        lote_num = i//BATCH_SIZE + 1
        total_lotes = (len(target_urls) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n[...] Lote {lote_num}/{total_lotes} ({len(batch)} perfiles)...")
        
        payload = {
            "targetUrls": batch,
            "maxPosts": 2,
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
                print(f"    [+] Recibidos {len(items)} items.")
                
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
            print(f"    [!] Error en lote {lote_num}: {e}")
            
        # Checkpoint parcial cada 5 lotes (guardar progreso en disco)
        if lote_num % 5 == 0 or i + BATCH_SIZE >= len(target_urls):
            updated_count = 0
            for c in all_connections:
                c_url = (c.get("url") or "").strip().lower().split('?')[0].rstrip('/')
                if c_url in all_results:
                    posts = all_results[c_url]
                    c["audit_status"] = "Activo Auditado"
                    c["last_updated_apify"] = "2026-08-01"
                    if posts:
                        p0 = posts[0]
                        posted_at = p0.get("postedAt", {})
                        c["last_post_date"] = posted_at.get("date", "Reciente")
                        c["last_post_text"] = p0.get("content") or "Publicación compartida"
                        author_info = p0.get("author", {})
                        if author_info.get("info"):
                            # VALIDACIÓN DE CHAMPION DRIFT (No sobrescribir a ciegas)
                            headline = author_info.get("info")
                            c["position_current"] = headline
                            # Si el titular menciona ex-empresa o nueva empresa
                            if c.get("company_zip", "").lower() not in headline.lower():
                                c["job_status"] = "🟡 Drift Detectado (Posible Cambio de Empresa)"
                            else:
                                c["job_status"] = "🟢 Vigente Confirmado"
                    else:
                        c["last_post_date"] = "Sin publicaciones recientes"
                        c["last_post_text"] = "Sin posts públicos"
                        c["job_status"] = "⚪ Inactivo en Posts"
                    updated_count += 1
                    
            with open(enriched_json, "w", encoding="utf-8") as f:
                json.dump(all_connections, f, indent=2, ensure_ascii=False)
            print(f"    💾 Checkpoint guardado: {updated_count} perfiles actualizados en disco.")

    print("\n✅ ¡AUDITORÍA Y ENRIQUECIMIENTO DE LA RED COMPLETA DE 3,119 CONTACTOS FINALIZADA CON ÉXITO!")

if __name__ == "__main__":
    main()
