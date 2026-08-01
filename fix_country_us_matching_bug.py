import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix the regex matching in getCoordsForContact so 'us' inside 'business' or 'accounting' does NOT match Estados Unidos!
old_us_check = "fullText.includes('us') || fullText.includes('usa') || fullText.includes('united states') || fullText.includes('miami')"
new_us_check = r"/\b(usa|united states|miami|new york|california|texas|florida)\b/i.test(fullText)"

if old_us_check in html:
    html = html.replace(old_us_check, new_us_check)
    print("✅ Bug de coincidencia de 'us' en palabras como 'business' o 'accounting' corregido en index.html.")

# Añadir empresas de la captura (Viva Aerobus, Mercado Libre, Mastercard) a COMPANY_LOCATION_DB en index.html y python
company_additions = """
    "viva aerobus": {"country": "México", "city": "Monterrey", "lat": 25.6866, "lng": -100.3161},
    "mercado libre": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "mercadolibre": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "mastercard": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
    "citibanamex": {"country": "México", "city": "CDMX", "lat": 19.4326, "lng": -99.1332},
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html actualizado exitosamente.")
