import os
import csv
import json
import urllib.request
import urllib.error
import sys
import zipfile
import io
import time
import concurrent.futures
import threading

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = '9018cc6af3d2949b4bd75bf4915ec4ae9eb46514'
progress_file = os.path.join(os.path.dirname(__file__), "serper_progress.json")
zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

def load_progress():
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"processed": {}}

def save_progress(progress):
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def fetch_serper(conn):
    url_clean = conn["url"].strip().lower().split('?')[0].rstrip('/')
    query = f"site:linkedin.com/in/ \"{conn['first_name']} {conn['last_name']}\""
    if url_clean:
        # Extraer el username de la URL
        parts = url_clean.split('linkedin.com/in/')
        if len(parts) > 1:
            username = parts[1].strip('/')
            query = f"site:linkedin.com/in/{username}"

    req_url = 'https://google.serper.dev/search'
    headers = {
        'X-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }
    data = json.dumps({'q': query}).encode('utf-8')
    req = urllib.request.Request(req_url, data=data, headers=headers)
    
    time.sleep(0.5) # Anti-rate limit
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            title = ""
            snippet = ""
            if 'organic' in res and len(res['organic']) > 0:
                title = res['organic'][0].get('title', '')
                snippet = res['organic'][0].get('snippet', '')
            return url_clean, {"status": "OK", "title": title, "snippet": snippet, "query": query}
    except Exception as e:
        return url_clean, {"status": "ERROR", "error": str(e), "query": query}

def main():
    print("=== INICIANDO EXTRACCIÓN MASIVA CON SERPER (2,500 BÚSQUEDAS) ===")
    
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
                            "first_name": row[0], "last_name": row[1], "url": row[2]
                        }
    except Exception as e:
        print(f"[!] Error leyendo Connections.csv: {e}")
        return

    progress = load_progress()
    to_fetch = []
    
    # Check what we already did with Apify
    apify_progress = {}
    apify_file = os.path.join(os.path.dirname(__file__), "audit_progress.json")
    if os.path.exists(apify_file):
        try:
            with open(apify_file, "r", encoding="utf-8") as f:
                apify_data = json.load(f)
                apify_progress = apify_data.get("processed_urls", {})
        except: pass

    for url, c in connections_map.items():
        if url not in progress["processed"] and url not in apify_progress:
            to_fetch.append(c)

    # Procesar todos los restantes
    print(f"[+] Quedan {len(to_fetch)} perfiles por procesar con Serper.")
    if not to_fetch:
        print("Todo procesado.")
        return

    lock = threading.Lock()
    count = 0
    total = len(to_fetch)
    
    print("Iniciando pool de threads (2 concurrencias)...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fetch_serper, c): c for c in to_fetch}
        for future in concurrent.futures.as_completed(futures):
            url_clean, result = future.result()
            
            with lock:
                progress["processed"][url_clean] = result
                count += 1
                if count % 100 == 0:
                    save_progress(progress)
                    print(f"  -> Progreso: {count} / {total} ({(count/total)*100:.1f}%)")
                    
    save_progress(progress)
    elapsed = time.time() - start_time
    print(f"\n[+] FINALIZADO. Procesados: {total}. Tiempo: {elapsed:.1f} segundos.")

if __name__ == "__main__":
    main()
