import os
import csv
import json
import urllib.request
import urllib.error
import sys
from datetime import datetime, timedelta

# Configurar stdout para usar UTF-8 en Windows y evitar errores de codificación
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de archivos
env_path = os.path.join(os.path.dirname(__file__), ".env")
connections_file = os.path.join(os.path.dirname(__file__), "connections_to_purge.csv")
progress_file = os.path.join(os.path.dirname(__file__), "audit_progress.json")
output_csv = os.path.join(os.path.dirname(__file__), "audited_connections.csv")

# Parámetros por defecto
BATCH_SIZE = 10     # URLs por cada llamada a Apify
RUN_LIMIT = 100     # Número máximo de contactos a auditar en esta ejecución
ACTIVO_DIAS = 90    # Considerar activo si publicó en los últimos 90 días

def load_env():
    """Reads local .env file without external dependencies."""
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def load_connections():
    """Loads connections to be audited from connections_to_purge.csv."""
    conns = []
    if not os.path.exists(connections_file):
        print(f"Error: No existe el archivo {connections_file}. Ejecuta primero clean_connections_offline.py.")
        return conns
        
    with open(connections_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Formatos de cabecera esperados: First Name, Last Name, Connected On, Company, Position, Email
            # El ZIP tiene URL, pero en connections_to_purge.csv mapeamos:
            # First Name, Last Name, Connected On, Company, Position, Email
            # Espera, necesitamos la URL. Vamos a buscar si en Connections.csv estaba la URL.
            # Sí, en Connections.csv estaba la URL. En connections_to_purge.csv necesitamos incluir la URL para poder rasparla.
            # Vamos a verificar si connections_to_purge.csv tiene la URL del perfil.
            conns.append(row)
    return conns

def load_progress():
    """Loads audit progress from JSON checkpoint file."""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "processed_urls": {},  # url -> {status, location, industry}
        "errors": {}           # url -> error_msg
    }

def save_progress(progress):
    """Saves audit progress to JSON checkpoint file."""
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def parse_date(date_str):
    # Formato: "04 Jul 2026"
    try:
        return datetime.strptime(date_str.strip(), "%d %b %Y")
    except Exception:
        return None

def main():
    print("=== AUDITORÍA MASIVA DE CONEXIONES CON APIFY (RIESGO CERO) ===")
    
    # 1. Cargar API Key
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    if not token or token == "tu_key_de_apify_aqui" or token == "":
        print("[!] ERROR: APIFY_API_TOKEN no configurado en el archivo .env.")
        return
        
    # 2. Cargar contactos
    # NOTA IMPORTANTE: En el connections_to_purge.csv original del script anterior olvidamos exportar la columna URL.
    # Vamos a verificar si está la URL. Si no, la extraemos directamente leyendo el Connections.csv original en caliente.
    # Esto es mucho más seguro para evitar errores en cascada.
    connections_map = {}
    zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
    
    import zipfile
    import io
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open('Connections.csv') as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                header = None
                for row in reader:
                    if len(row) > 0 and 'First Name' in row:
                        header = row
                        break
                
                # Mapear URL a su fila
                for row in reader:
                    if len(row) < 7:
                        continue
                    url = row[2].strip().lower().split('?')[0].rstrip('/')
                    if url:
                        connections_map[url] = {
                            "first_name": row[0],
                            "last_name": row[1],
                            "url": row[2],
                            "company": row[4],
                            "position": row[5],
                            "connected_on": row[6]
                        }
    except Exception as e:
        print(f"[!] Error leyendo Connections.csv del ZIP: {e}")
        return

    # 3. Cargar el listado de candidatos a purgar (con 0 mensajes) para filtrar
    if not os.path.exists(connections_file):
        print(f"[!] No se encontró el archivo {connections_file}. Ejecuta clean_connections_offline.py primero.")
        return
        
    purge_names = set()
    with open(connections_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Guardamos el identificador del nombre para cruzar
            purge_names.add(f"{row['First Name'].strip().lower()} {row['Last Name'].strip().lower()}")

    # 4. Filtrar conexiones mudas de 2017 a 2022
    candidates = []
    for url, conn in connections_map.items():
        name_key = f"{conn['first_name'].strip().lower()} {conn['last_name'].strip().lower()}"
        if name_key in purge_names:
            # Es un contacto mudo. Ahora verifiquemos el año de conexión.
            conn_date = parse_date(conn["connected_on"])
            if conn_date and conn_date.year in [2017, 2018, 2019, 2020, 2021, 2022]:
                candidates.append(conn)

    print(f"\n[+] Se encontraron {len(candidates)} conexiones mudas de los años 2017-2022.")
    if not candidates:
        print("No hay candidatos que auditar para este periodo.")
        return

    # 5. Cargar progreso del checkpoint
    progress = load_progress()
    processed_count = len(progress["processed_urls"])
    print(f"[+] Progreso cargado: {processed_count} perfiles ya auditados en sesiones anteriores.")
    
    # Filtrar candidatos que ya fueron procesados o dieron error persistente
    to_audit = []
    for c in candidates:
        url_clean = c["url"].strip().lower().split('?')[0].rstrip('/')
        if url_clean not in progress["processed_urls"] and url_clean not in progress["errors"]:
            to_audit.append(c)
            
    print(f"[+] Quedan {len(to_audit)} perfiles pendientes por auditar.")
    
    if not to_audit:
        print("¡Todos los candidatos de 2025 y 2026 ya han sido auditados!")
        write_final_csv(progress, connections_map)
        return
        
    # Limitar el número de auditorías de esta corrida
    run_batch = to_audit[:RUN_LIMIT]
    print(f"\n[!] Ejecución programada: Se auditarán {len(run_batch)} perfiles en esta corrida (Límite: {RUN_LIMIT}).")
    print(f"    Esto consumirá aproximadamente {len(run_batch) / BATCH_SIZE * 0.1:.2f} Compute Units de Apify.")
    
    # 6. Procesar en lotes (Batching)
    actor_id = "harvestapi~linkedin-profile-scraper"
    
    for i in range(0, len(run_batch), BATCH_SIZE):
        batch = run_batch[i:i+BATCH_SIZE]
        batch_urls = [c["url"] for c in batch]
        
        print(f"\n---> Procesando lote {i//BATCH_SIZE + 1} ({len(batch)} perfiles)...")
        for u in batch_urls:
            print(f"  * {u}")
            
        payload = {
            "urls": batch_urls,
            "minDelay": 1,
            "maxDelay": 5
        }
        
        data_bytes = json.dumps(payload).encode("utf-8")
        url_api = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
        
        req = urllib.request.Request(
            url_api,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=360) as response:
                res_body = response.read().decode("utf-8")
                items = json.loads(res_body)
                
                # Guardar items brutos
                os.makedirs('raw_apify_profiles', exist_ok=True)
                with open(f'raw_apify_profiles/batch_{i//BATCH_SIZE + 1}.json', 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                # Mapear los resultados
                profile_data = {}
                for item in items:
                    if not item or not isinstance(item, dict):
                        continue
                    # Obtener la url solicitada a través de "originalQuery"
                    orig_query = item.get("originalQuery", {})
                    target_url = orig_query.get("url") or item.get("linkedinUrl")
                    
                    if target_url:
                        target_url_clean = target_url.strip().lower().split('?')[0].rstrip('/')
                        profile_data[target_url_clean] = item
                
                # Clasificar cada perfil del lote
                for c in batch:
                    c_url_clean = c["url"].strip().lower().split('?')[0].rstrip('/')
                    profile = profile_data.get(c_url_clean)
                    
                    if not profile or profile.get('error'):
                        # No tiene perfil o dio error
                        progress["processed_urls"][c_url_clean] = {
                            "status": "No Encontrado",
                            "location": "Desconocido",
                            "industry": "Desconocido"
                        }
                    else:
                        # Encontrar ubicación e industria
                        loc = profile.get('location', {})
                        loc_text = loc.get('linkedinText', 'Desconocido') if isinstance(loc, dict) else (loc or "Desconocido")
                        
                        industry = profile.get('industry')
                        if not industry and profile.get('experience'):
                            industry = profile['experience'][0].get('companyName')
                        
                        progress["processed_urls"][c_url_clean] = {
                            "status": "Extraído",
                            "location": loc_text,
                            "industry": industry or "Desconocido"
                        }
                        
                    print(f"  -> Resultado {c['first_name']} {c['last_name']}: {progress['processed_urls'][c_url_clean]['status']} (Loc: {progress['processed_urls'][c_url_clean]['location']})")
                    
        except urllib.error.HTTPError as e:
            err_msg = f"HTTP Error {e.code}"
            print(f"  [!] Error en lote: {err_msg}")
            for c in batch:
                c_url_clean = c["url"].strip().lower().split('?')[0].rstrip('/')
                progress["errors"][c_url_clean] = err_msg
        except Exception as e:
            err_msg = str(e)
            print(f"  [!] Error inesperado en lote: {err_msg}")
            for c in batch:
                c_url_clean = c["url"].strip().lower().split('?')[0].rstrip('/')
                progress["errors"][c_url_clean] = err_msg
                
        # Guardar progreso parcial al finalizar cada lote
        save_progress(progress)
        
    # 7. Escribir resultados finales en CSV consolidado
    write_final_csv(progress, connections_map)

def write_final_csv(progress, connections_map):
    """Writes the final consolidated audited list to audited_connections.csv."""
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["First Name", "Last Name", "URL", "Connected On", "Company", "Position", "Audit Status", "Location", "Industry"])
        
        extraidos = 0
        no_encontrados = 0
        
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
                if data["status"] == "Extraído":
                    extraidos += 1
                else:
                    no_encontrados += 1
                    
        print(f"\n[+] Auditoría terminada. CSV exportado a: {output_csv}")
        print(f"    - Perfiles extraídos: {extraidos}")
        print(f"    - Perfiles no encontrados: {no_encontrados}")

if __name__ == "__main__":
    main()
