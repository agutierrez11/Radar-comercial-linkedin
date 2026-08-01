import csv
import json
import re
import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

# Diccionario de sedes de empresas conocidas (LATAM y Globales)
COMPANY_LOCATION_DB = {
    "clip": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "konfío": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "konfio": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "mercado libre": {"country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lng": -58.3816},
    "mercadolibre": {"country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lng": -58.3816},
    "nubank": {"country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lng": -46.6333},
    "nu méxico": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "nu mexico": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "exante": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "go4more": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "ve commercial vehicles ltd.": {"country": "India", "city": "Gurugram", "lat": 28.4595, "lng": 77.0266},
    "data mechanics pvt ltd": {"country": "Pakistán", "city": "Lahore", "lat": 31.5204, "lng": 74.3587},
    "itio innovex pvt. ltd.": {"country": "India", "city": "Noida", "lat": 28.5355, "lng": 77.3910},
    "kavak": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "rappi": {"country": "Colombia", "city": "Bogotá", "lat": 4.7110, "lng": -74.0721},
    "clara": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "bitso": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "stori": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "platzi": {"country": "Colombia", "city": "Bogotá", "lat": 4.7110, "lng": -74.0721},
    "globant": {"country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lng": -58.3816},
    "banco santander": {"country": "España", "city": "Madrid", "lat": 40.4168, "lng": -3.7038},
    "bbva": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "banorte": {"country": "México", "city": "Monterrey", "lat": 25.6866, "lng": -100.3161},
    "femsa": {"country": "México", "city": "Monterrey", "lat": 25.6866, "lng": -100.3161},
    "bancolombia": {"country": "Colombia", "city": "Medellín", "lat": 6.2442, "lng": -75.5812},
    "falabella": {"country": "Chile", "city": "Santiago", "lat": -33.4489, "lng": -70.6693},
    "copec": {"country": "Chile", "city": "Santiago", "lat": -33.4489, "lng": -70.6693},
    "stoneco": {"country": "Brasil", "city": "Rio de Janeiro", "lat": -22.9068, "lng": -43.1729},
    "pagseguro": {"country": "Brasil", "city": "São Paulo", "lat": -23.5505, "lng": -46.6333},
}

COUNTRY_COORDS = {
    "México": {"lat": 23.6345, "lng": -102.5528},
    "Colombia": {"lat": 4.5709, "lng": -74.2973},
    "Argentina": {"lat": -38.4161, "lng": -63.6167},
    "Chile": {"lat": -35.6751, "lng": -71.5430},
    "Brasil": {"lat": -14.2350, "lng": -51.9253},
    "España": {"lat": 40.4637, "lng": -3.7492},
    "Estados Unidos": {"lat": 37.0902, "lng": -95.7129},
    "India": {"lat": 20.5937, "lng": 78.9629},
    "Pakistán": {"lat": 30.3753, "lng": 69.3451},
    "Perú": {"lat": -9.1900, "lng": -75.0152},
    "Ecuador": {"lat": -1.8312, "lng": -78.1834},
    "Uruguay": {"lat": -32.5228, "lng": -55.7658},
    "Desconocido": {"lat": 19.4326, "lng": -99.1332}
}

def remove_diacritics(text):
    if not text:
        return ""
    nfkd_form = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

def infer_location_and_status(first_name, last_name, company, position, connected_on_str):
    company_clean = remove_diacritics(company)
    position_clean = remove_diacritics(position)
    full_text = f"{company_clean} {position_clean}"
    
    country = "Desconocido"
    city = "Desconocido"
    lat = 19.4326
    lng = -99.1332
    
    for key, val in COMPANY_LOCATION_DB.items():
        if key in company_clean:
            country = val["country"]
            city = val["city"]
            lat = val["lat"]
            lng = val["lng"]
            break
            
    if country == "Desconocido":
        if "mexico" in full_text or "cdmx" in full_text or "cancun" in full_text or "monterrey" in full_text or "guadalajara" in full_text:
            country = "México"
            city = "CDMX" if "cdmx" in full_text else ("Cancún" if "cancun" in full_text else "Ciudad")
        elif "colombia" in full_text or "bogota" in full_text or "medellin" in full_text:
            country = "Colombia"
            city = "Bogotá"
        elif "argentina" in full_text or "buenos aires" in full_text:
            country = "Argentina"
            city = "Buenos Aires"
        elif "chile" in full_text or "santiago" in full_text:
            country = "Chile"
            city = "Santiago"
        elif "espana" in full_text or "madrid" in full_text or "barcelona" in full_text:
            country = "España"
            city = "Madrid"
        elif "us" in full_text or "usa" in full_text or "united states" in full_text or "miami" in full_text or "new york" in full_text:
            country = "Estados Unidos"
            city = "Miami"
        elif "india" in full_text:
            country = "India"
            city = "Delhi"
        elif "pakistan" in full_text:
            country = "Pakistán"
            city = "Lahore"
            
    if country in COUNTRY_COORDS and (lat == 19.4326 and lng == -99.1332 and country != "México"):
        lat = COUNTRY_COORDS[country]["lat"]
        lng = COUNTRY_COORDS[country]["lng"]
        
    recency_status = "🟢 Vigente Confirmado"
    if "2026" in connected_on_str:
        recency_status = "🟢 Vigente Confirmado"
    elif "2025" in connected_on_str or "2024" in connected_on_str:
        recency_status = "🟡 Vigente Probable"
    else:
        recency_status = "🔍 Por Corroborar"
        
    if not company:
        recency_status = "⚠️ Sin Empresa Registrada"
        
    return {
        "country": country,
        "city": city,
        "lat": lat,
        "lng": lng,
        "job_status": recency_status,
        "is_current": True if "Vigente" in recency_status else False
    }

def process_all_connections():
    csv_file = "audited_connections.csv"
    output_json = "enriched_connections.json"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} no existe.")
        return
        
    enriched_data = []
    
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            first = row.get("First Name", "").strip()
            last = row.get("Last Name", "").strip()
            url = row.get("URL", "").strip()
            connected_on = row.get("Connected On", "").strip()
            company = row.get("Company", "").strip()
            position = row.get("Position", "").strip()
            audit_status = row.get("Audit Status", "").strip()
            last_post = row.get("Last Post Date", "").strip()
            
            location_info = infer_location_and_status(first, last, company, position, connected_on)
            
            item = {
                "id": i + 1,
                "first_name": first,
                "last_name": last,
                "full_name": f"{first} {last}".strip(),
                "url": url,
                "connected_on": connected_on,
                "company": company if company else "Empresa No Especificada",
                "position": position if position else "Cargo No Especificado",
                "audit_status": audit_status,
                "last_post_date": last_post,
                "country": location_info["country"],
                "city": location_info["city"],
                "lat": location_info["lat"],
                "lng": location_info["lng"],
                "job_status": location_info["job_status"],
                "is_current": location_info["is_current"]
            }
            enriched_data.append(item)
            
    print(f"✅ Procesadas {len(enriched_data)} conexiones sin costo alguno (Zero Cost).")
    
    with open(output_json, "w", encoding="utf-8") as f_out:
        json.dump(enriched_data, f_out, ensure_ascii=False, indent=2)
        
    print(f" Archivo listo: '{output_json}' con coordenadas, recencia y ubicaciones normalizadas.")
    return enriched_data

if __name__ == "__main__":
    process_all_connections()
