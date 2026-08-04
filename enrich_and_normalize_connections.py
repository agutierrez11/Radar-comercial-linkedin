import csv
import json
import re
import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

# Diccionario de sedes de empresas conocidas (LATAM, Europa y Globales)
COMPANY_LOCATION_DB = {
    # LATAM
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
    "kavak": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "rappi": {"country": "Colombia", "city": "Bogotá", "lat": 4.7110, "lng": -74.0721},
    "clara": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "bitso": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "stori": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "platzi": {"country": "Colombia", "city": "Bogotá", "lat": 4.7110, "lng": -74.0721},
    "globant": {"country": "Argentina", "city": "Buenos Aires", "lat": -34.6037, "lng": -58.3816},
    "bbva": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "banorte": {"country": "México", "city": "Monterrey", "lat": 25.6866, "lng": -100.3161},
    "femsa": {"country": "México", "city": "Monterrey", "lat": 25.6866, "lng": -100.3161},
    "bancolombia": {"country": "Colombia", "city": "Medellín", "lat": 6.2442, "lng": -75.5812},
    "falabella": {"country": "Chile", "city": "Santiago", "lat": -33.4489, "lng": -70.6693},

    # EUROPA
    "banco santander": {"country": "España", "city": "Madrid", "lat": 40.4168, "lng": -3.7038},
    "revolut": {"country": "Reino Unido", "city": "Londres", "lat": 51.5074, "lng": -0.1278},
    "klarna": {"country": "Suecia", "city": "Estocolmo", "lat": 59.3293, "lng": 18.0686},
    "n26": {"country": "Alemania", "city": "Berlín", "lat": 52.5200, "lng": 13.4050},
    "sap": {"country": "Alemania", "city": "Walldorf", "lat": 49.2936, "lng": 8.6416},
    "spotify": {"country": "Suecia", "city": "Estocolmo", "lat": 59.3293, "lng": 18.0686},
    "asml": {"country": "Países Bajos", "city": "Veldhoven", "lat": 51.4173, "lng": 5.4072},
    "adyen": {"country": "Países Bajos", "city": "Ámsterdam", "lat": 52.3676, "lng": 4.9041},
    "delivery hero": {"country": "Alemania", "city": "Berlín", "lat": 52.5200, "lng": 13.4050},
    "siemens": {"country": "Alemania", "city": "Múnich", "lat": 48.1351, "lng": 11.5820},
    "airbus": {"country": "Francia", "city": "Toulouse", "lat": 43.6047, "lng": 1.4442},
    "l'oréal": {"country": "Francia", "city": "París", "lat": 48.8566, "lng": 2.3522},
    "loreal": {"country": "Francia", "city": "París", "lat": 48.8566, "lng": 2.3522},
    "nestlé": {"country": "Suiza", "city": "Vevey", "lat": 46.4628, "lng": 6.8419},
    "nestle": {"country": "Suiza", "city": "Vevey", "lat": 46.4628, "lng": 6.8419},

    # ASIA / OTROS
    "ve commercial vehicles ltd.": {"country": "India", "city": "Gurugram", "lat": 28.4595, "lng": 77.0266},
    "data mechanics pvt ltd": {"country": "Pakistán", "city": "Lahore", "lat": 31.5204, "lng": 74.3587},
    "itio innovex pvt. ltd.": {"country": "India", "city": "Noida", "lat": 28.5355, "lng": 77.3910},
}

COUNTRY_COORDS = {
    # América
    "México": {"lat": 23.6345, "lng": -102.5528},
    "Colombia": {"lat": 4.5709, "lng": -74.2973},
    "Argentina": {"lat": -38.4161, "lng": -63.6167},
    "Chile": {"lat": -35.6751, "lng": -71.5430},
    "Brasil": {"lat": -14.2350, "lng": -51.9253},
    "Estados Unidos": {"lat": 37.0902, "lng": -95.7129},
    "Perú": {"lat": -9.1900, "lng": -75.0152},
    "Ecuador": {"lat": -1.8312, "lng": -78.1834},
    "Uruguay": {"lat": -32.5228, "lng": -55.7658},
    "Costa Rica": {"lat": 9.7489, "lng": -83.7534},
    "Panamá": {"lat": 8.5379, "lng": -80.7821},
    "El Salvador": {"lat": 13.7941, "lng": -88.8965},
    "Guatemala": {"lat": 15.7834, "lng": -90.2307},
    "Honduras": {"lat": 15.1999, "lng": -86.2419},
    "Nicaragua": {"lat": 12.8654, "lng": -85.2072},

    # Europa
    "España": {"lat": 40.4637, "lng": -3.7492},
    "Reino Unido": {"lat": 55.3781, "lng": -3.4360},
    "Alemania": {"lat": 51.1657, "lng": 10.4515},
    "Francia": {"lat": 46.2276, "lng": 2.2137},
    "Italia": {"lat": 41.8719, "lng": 12.5674},
    "Países Bajos": {"lat": 52.1326, "lng": 5.2913},
    "Suiza": {"lat": 46.8182, "lng": 8.2275},
    "Suecia": {"lat": 60.1282, "lng": 18.6435},
    "Portugal": {"lat": 39.3999, "lng": -8.2245},
    "Irlanda": {"lat": 53.4129, "lng": -8.2439},
    "Bélgica": {"lat": 50.5039, "lng": 4.4699},
    "Austria": {"lat": 47.5162, "lng": 14.5501},
    "Polonia": {"lat": 51.9194, "lng": 19.1451},
    "Dinamarca": {"lat": 56.2639, "lng": 9.5018},
    "Noruega": {"lat": 60.4720, "lng": 8.4689},
    "Finlandia": {"lat": 61.9241, "lng": 25.7482},

    # Asia & Global
    "India": {"lat": 20.5937, "lng": 78.9629},
    "Pakistán": {"lat": 30.3753, "lng": 69.3451},
    "Desconocido": {"lat": 19.4326, "lng": -99.1332}
}

def remove_diacritics(text):
    if not text:
        return ""
    nfkd_form = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

def infer_seniority(position):
    if not position:
        return "Desconocido"
    pos = remove_diacritics(position)
    
    # C-Level / Founder
    if re.search(r'\b(founder|co-founder|ceo|cfo|coo|cto|cmo|cio|ciso|cro|chro|chief|presidente|president|owner|dueno|socio|partner)\b', pos):
        return "C-Level / Founder"
    
    # VP / Director
    if re.search(r'\b(vp|vice president|vicepresidente|director|head|jefe)\b', pos):
        return "VP / Director"
        
    # Manager
    if re.search(r'\b(manager|gerente|lead|leader|supervisor|coordinator|coordinador)\b', pos):
        return "Manager"
        
    # Entry Level / IC
    if re.search(r'\b(analyst|analista|specialist|especialista|engineer|ingeniero|developer|desarrollador|consultant|consultor|executive|ejecutivo|associate|asociado|assistant|asistente)\b', pos):
        return "Individual Contributor"
        
    return "Desconocido"


def infer_location_and_status(first_name, last_name, company, position, connected_on_str):
    company_clean = remove_diacritics(company)
    position_clean = remove_diacritics(position)
    full_text = f"{company_clean} {position_clean}"
    
    country = "Desconocido"
    city = "Desconocido"
    lat = 19.4326
    lng = -99.1332
    
    # 1. Match en BD de Sedes
    for key, val in COMPANY_LOCATION_DB.items():
        if key in company_clean:
            country = val["country"]
            city = val["city"]
            lat = val["lat"]
            lng = val["lng"]
            break
            
    # 2. Match por palabras clave geográficas en América, Europa, Asia
    if country == "Desconocido":
        # América
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
        elif re.search(r'\b(usa|united states|miami|new york|california|texas|florida)\b', full_text):
            country = "Estados Unidos"
            city = "Miami"
        elif "panama" in full_text:
            country = "Panamá"
            city = "Panamá"
        elif "costa rica" in full_text or "san jose" in full_text:
            country = "Costa Rica"
            city = "San José"
        elif "el salvador" in full_text or "san salvador" in full_text:
            country = "El Salvador"
            city = "San Salvador"
        elif "guatemala" in full_text:
            country = "Guatemala"
            city = "Guatemala"
        elif "honduras" in full_text or "tegucigalpa" in full_text or "san pedro sula" in full_text:
            country = "Honduras"
            city = "Tegucigalpa"
        elif "nicaragua" in full_text or "managua" in full_text:
            country = "Nicaragua"
            city = "Managua"
        elif "peru" in full_text or "lima" in full_text:
            country = "Perú"
            city = "Lima"
        elif "ecuador" in full_text or "quito" in full_text or "guayaquil" in full_text:
            country = "Ecuador"
            city = "Quito"
        elif "uruguay" in full_text or "montevideo" in full_text:
            country = "Uruguay"
            city = "Montevideo"
            
        # Europa
        elif "espana" in full_text or "spain" in full_text or "madrid" in full_text or "barcelona" in full_text:
            country = "España"
            city = "Madrid" if "madrid" in full_text else "Barcelona"
        elif "uk" in full_text or "united kingdom" in full_text or "london" in full_text or "londres" in full_text or "manchester" in full_text:
            country = "Reino Unido"
            city = "Londres"
        elif "germany" in full_text or "alemania" in full_text or "berlin" in full_text or "munich" in full_text or "frankfurt" in full_text:
            country = "Alemania"
            city = "Berlín"
        elif "france" in full_text or "francia" in full_text or "paris" in full_text or "lyon" in full_text:
            country = "Francia"
            city = "París"
        elif "italy" in full_text or "italia" in full_text or "rome" in full_text or "milan" in full_text or "roma" in full_text:
            country = "Italia"
            city = "Milán"
        elif "netherlands" in full_text or "paises bajos" in full_text or "amsterdam" in full_text or "rotterdam" in full_text:
            country = "Países Bajos"
            city = "Ámsterdam"
        elif "switzerland" in full_text or "suiza" in full_text or "zurich" in full_text or "geneva" in full_text:
            country = "Suiza"
            city = "Zúrich"
        elif "sweden" in full_text or "suecia" in full_text or "stockholm" in full_text:
            country = "Suecia"
            city = "Estocolmo"
        elif "portugal" in full_text or "lisbon" in full_text or "lisboa" in full_text:
            country = "Portugal"
            city = "Lisboa"
        elif "ireland" in full_text or "irlanda" in full_text or "dublin" in full_text:
            country = "Irlanda"
            city = "Dublín"

        # Asia
        elif "india" in full_text:
            country = "India"
            city = "Delhi"
        elif "pakistan" in full_text:
            country = "Pakistán"
            city = "Lahore"

    # Coordenadas de respaldo por país
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
            
    print(f"✅ Procesadas {len(enriched_data)} conexiones con soporte extendido para Europa y América.")
    
    with open(output_json, "w", encoding="utf-8") as f_out:
        json.dump(enriched_data, f_out, ensure_ascii=False, indent=2)
        
    return enriched_data

if __name__ == "__main__":
    process_all_connections()
