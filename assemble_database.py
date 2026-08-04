import os
import csv
import json
import zipfile
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
apify_file = "audit_progress.json"
serper_file = "serper_progress.json"
output_csv = "radar_database_final.csv"

# Diccionario simple de países clave para buscar en el snippet
COUNTRIES = [
    "Mexico", "México", "Colombia", "Argentina", "Chile", "Peru", "Perú", 
    "Ecuador", "Venezuela", "Uruguay", "Paraguay", "Bolivia", 
    "Panama", "Panamá", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Nicaragua",
    "Spain", "España", "United States", "USA", "Estados Unidos", "UK", "Canada", "Brazil", "Brasil"
]

def extract_location_from_snippet(snippet):
    snip_lower = snippet.lower()
    for country in COUNTRIES:
        if country.lower() in snip_lower:
            return country
    return "Desconocido"

def main():
    print("=== ENSAMBLANDO BASE DE DATOS FINAL ===")
    
    apify_data = {}
    if os.path.exists(apify_file):
        with open(apify_file, "r", encoding="utf-8") as f:
            apify_data = json.load(f).get("processed_urls", {})
            
    serper_data = {}
    if os.path.exists(serper_file):
        with open(serper_file, "r", encoding="utf-8") as f:
            serper_data = json.load(f).get("processed", {})
            
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
                            "first_name": row[0],
                            "last_name": row[1],
                            "url": row[2],
                            "company": row[4],
                            "position": row[5],
                            "connected_on": row[6]
                        }
    except Exception as e:
        print("Error leyendo ZIP:", e)
        return
        
    print(f"Contactos en ZIP: {len(connections_map)}")
    
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["First Name", "Last Name", "URL", "Connected On", "Company", "Position", "Data Source", "Location", "Google Snippet"])
        
        apify_count = 0
        serper_count = 0
        missing_count = 0
        
        for url, conn in connections_map.items():
            source = "ZIP (No Data)"
            loc = "Desconocido"
            snippet = ""
            
            if url in apify_data and apify_data[url].get("status") == "Extraído":
                source = "Apify"
                loc = apify_data[url].get("location", "Desconocido")
                apify_count += 1
            elif url in serper_data and serper_data[url].get("status") == "OK":
                source = "Google Serper"
                snippet = serper_data[url].get("snippet", "")
                loc = extract_location_from_snippet(snippet)
                serper_count += 1
            else:
                missing_count += 1
                
            writer.writerow([
                conn["first_name"],
                conn["last_name"],
                conn["url"],
                conn["connected_on"],
                conn["company"],
                conn["position"],
                source,
                loc,
                snippet
            ])
            
    print(f"\n[+] Ensamblaje completado en {output_csv}")
    print(f" - Datos de Apify: {apify_count}")
    print(f" - Datos de Google Serper: {serper_count}")
    print(f" - Sin datos (Faltantes): {missing_count}")
    print(f" - Total Base de Datos: {apify_count + serper_count + missing_count}")

if __name__ == "__main__":
    main()
