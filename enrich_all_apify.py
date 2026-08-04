import os
import csv
import json
import urllib.request
import urllib.error
import sys
import zipfile
import io
import time

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
progress_file = os.path.join(os.path.dirname(__file__), "audit_progress.json")
output_csv = os.path.join(os.path.dirname(__file__), "all_connections_enriched.csv")
zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
raw_dir = os.path.join(os.path.dirname(__file__), "raw_apify_profiles")

ACTOR_ID = "harvestapi~linkedin-profile-scraper"
BATCH_SIZE = 170

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

def load_progress():
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"processed_urls": {}, "errors": {}}

def save_progress(progress):
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def write_final_csv(progress, connections_map):
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["First Name", "Last Name", "URL", "Connected On", "Company", "Position", "Audit Status", "Location", "Industry"])
        for url_clean, data in progress["processed_urls"].items():
            conn = connections_map.get(url_clean)
            if conn:
                writer.writerow([
                    conn["first_name"],
                    conn["last_name"],
                    conn["url"],
                    conn["connected_on"],
                    conn["company"],
                    conn["position"],
                    data["status"],
                    data.get("location", "Desconocido"),
                    data.get("industry", "Desconocido")
                ])

def main():
    print("=== EXTRACCIÓN MASIVA 3.0 (LOTES ASÍNCRONOS SEGUROS) ===")
    
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    
    connections_map = {}
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open('Connections.csv') as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                for row in reader:
                    if len(row) > 0 and 'First Name' in row: break
                for row in reader:
                    if len(row) < 7: continue
                    url = row[2].strip().lower().split('?')[0].rstrip('/')
                    if url:
                        connections_map[url] = {
                            "first_name": row[0], "last_name": row[1], "url": row[2],
                            "company": row[4], "position": row[5], "connected_on": row[6]
                        }
    except Exception as e:
        print(f"[!] Error leyendo Connections.csv: {e}")
        return

    progress = load_progress()
    to_audit = []
    for url, c in connections_map.items():
        if url not in progress["processed_urls"] and url not in progress["errors"]:
            to_audit.append(c)
            
    print(f"[+] Quedan {len(to_audit)} perfiles pendientes por extraer.")
    if not to_audit:
        write_final_csv(progress, connections_map)
        return
        
    os.makedirs(raw_dir, exist_ok=True)
    
    total_batches = (len(to_audit) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"[!] Se dividirán en {total_batches} lotes (consumirá {total_batches} Runs de Apify).")
    
    for i in range(0, len(to_audit), BATCH_SIZE):
        batch = to_audit[i:i+BATCH_SIZE]
        batch_urls = [c["url"] for c in batch]
        batch_num = (i // BATCH_SIZE) + 1
        
        print(f"\n---> Iniciando Lote {batch_num}/{total_batches} ({len(batch)} perfiles)...")
        
        payload = {"urls": batch_urls, "minDelay": 1, "maxDelay": 4}
        data_bytes = json.dumps(payload).encode("utf-8")
        
        url_start = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={token}"
        req = urllib.request.Request(url_start, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        
        try:
            with urllib.request.urlopen(req) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                run_id = res_json['data']['id']
                dataset_id = res_json['data']['defaultDatasetId']
                print(f"  [+] Run ID: {run_id}")
        except Exception as e:
            print(f"  [!] Error iniciando el Lote {batch_num}: {e}")
            break
            
        url_status = f"https://api.apify.com/v2/actor-runs/{run_id}?token={token}"
        status = "UNKNOWN"
        while True:
            try:
                req_status = urllib.request.Request(url_status)
                with urllib.request.urlopen(req_status) as response:
                    status_data = json.loads(response.read().decode("utf-8"))
                    status = status_data['data']['status']
                    if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                        break
            except:
                pass
            time.sleep(30)
            
        print(f"  [+] Lote terminó con estado: {status}")
        
        if status != 'SUCCEEDED':
            print("  [!] Hubo un problema con este Run. Deteniendo proceso.")
            break
            
        url_dataset = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}"
        try:
            req_dataset = urllib.request.Request(url_dataset)
            with urllib.request.urlopen(req_dataset) as response:
                items = json.loads(response.read().decode("utf-8"))
                
                with open(os.path.join(raw_dir, f"lote_{batch_num}_{run_id}.json"), 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                    
                profile_data = {}
                for item in items:
                    if not item or not isinstance(item, dict): continue
                    orig_query = item.get("originalQuery", {})
                    target_url = orig_query.get("url") or item.get("linkedinUrl")
                    if target_url:
                        target_url_clean = target_url.strip().lower().split('?')[0].rstrip('/')
                        profile_data[target_url_clean] = item
                        
                for c in batch:
                    c_url_clean = c["url"].strip().lower().split('?')[0].rstrip('/')
                    profile = profile_data.get(c_url_clean)
                    if not profile or profile.get('error'):
                        progress["processed_urls"][c_url_clean] = {"status": "No Encontrado", "location": "Desconocido", "industry": "Desconocido"}
                    else:
                        loc = profile.get('location', {})
                        loc_text = loc.get('linkedinText', 'Desconocido') if isinstance(loc, dict) else (loc or "Desconocido")
                        industry = profile.get('industry')
                        if not industry and profile.get('experience'):
                            industry = profile['experience'][0].get('companyName')
                        progress["processed_urls"][c_url_clean] = {"status": "Extraído", "location": loc_text, "industry": industry or "Desconocido"}
                        
                save_progress(progress)
                write_final_csv(progress, connections_map)
                print(f"  [+] Lote {batch_num} guardado con éxito. ({len(items)} items procesados)")
        except Exception as e:
            print(f"  [!] Error descargando dataset del Lote {batch_num}: {e}")
            
    print("\n[+] EXTRACCIÓN MASIVA FINALIZADA.")

if __name__ == "__main__":
    main()
