import zipfile
import csv
import json
import hashlib
import os
import sys
import urllib.request
from dotenv import load_dotenv

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
SUPABASE_URL = "https://hsrseeqhdtogpdqbveay.supabase.co"
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip('"')

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json"
}

def generate_contact_id(vault_id, url, name, connected_on):
    clean_url = (url or '').strip().lower().rstrip('/')
    if clean_url and 'linkedin.com/in/' in clean_url:
        slug = clean_url.split('linkedin.com/in/')[-1].split('?')[0].split('/')[0]
        slug_hash = hashlib.md5(slug.encode('utf-8')).hexdigest()[:12]
        return f"{vault_id}_{slug_hash}"
    clean_name = (name or '').strip().lower()
    clean_date = (connected_on or '').strip().lower()
    comp = f"{clean_name}_{clean_date}".encode('utf-8')
    return f"{vault_id}_{hashlib.md5(comp).hexdigest()[:12]}"

def infer_country(email, company, position):
    blob = f"{email} {company} {position}".lower()
    if '.mx' in blob or 'mexico' in blob or 'cdmx' in blob or 'monterrey' in blob or 'guadalajara' in blob: return 'México'
    if '.co' in blob or 'colombia' in blob or 'bogota' in blob or 'medellin' in blob: return 'Colombia'
    if '.cl' in blob or 'chile' in blob or 'santiago' in blob: return 'Chile'
    if '.pe' in blob or 'peru' in blob or 'lima' in blob: return 'Perú'
    if '.ar' in blob or 'argentina' in blob or 'buenos aires' in blob: return 'Argentina'
    if '.es' in blob or 'espana' in blob or 'spain' in blob or 'madrid' in blob or 'barcelona' in blob: return 'España'
    if '.br' in blob or 'brasil' in blob or 'sao paulo' in blob: return 'Brasil'
    if 'usa' in blob or 'united states' in blob or 'miami' in blob: return 'Estados Unidos'
    return 'Desconocido'

def infer_hierarchy(pos):
    p = (pos or '').lower()
    if any(k in p for k in ['ceo', 'cfo', 'cto', 'coo', 'founder', 'fundador', 'director general', 'presidente']): return 'C-Level'
    if any(k in p for k in ['director', 'head', 'vp', 'vice president']): return 'Director'
    if any(k in p for k in ['gerente', 'manager', 'lead', 'jefe', 'responsable']): return 'Gerente'
    return 'Otros'

def infer_sector(pos, company):
    b = f"{pos} {company}".lower()
    if any(k in b for k in ['fintech', 'pago', 'pay', 'bank', 'banco', 'tarjeta', 'card', 'clip', 'fiserv', 'stripe']): return 'Fintech/Pagos'
    if any(k in b for k in ['retail', 'ecommerce', 'tienda', 'walmart', 'liverpool']): return 'Retail/eCommerce'
    if any(k in b for k in ['software', 'saas', 'tech', 'cloud', 'ai', 'ia']): return 'SaaS/Tech'
    return 'Otro'

COUNTRY_COORDS = {
    "México": {"lat": 19.4326, "lng": -99.1332},
    "Colombia": {"lat": 4.5709, "lng": -74.2973},
    "Chile": {"lat": -35.6751, "lng": -71.5430},
    "Perú": {"lat": -9.1900, "lng": -75.0152},
    "Argentina": {"lat": -38.4161, "lng": -63.6167},
    "España": {"lat": 40.4637, "lng": -3.7492},
    "Brasil": {"lat": -14.2350, "lng": -51.9253},
    "Estados Unidos": {"lat": 37.0902, "lng": -95.7129},
    "Desconocido": {"lat": 19.4326, "lng": -99.1332}
}

def build_unified_contacts(zip_path):
    vault_id = "vault_antonio"
    if not os.path.exists(zip_path):
        print(f"❌ Error: El archivo ZIP no existe en {zip_path}")
        return None

    harvest_file = "los_404_contactos_harvest_reales.json"
    with open(harvest_file, "r", encoding="utf-8") as f:
        harvest_data = json.load(f)

    h_by_url = {}
    h_by_comp = {}
    for h in harvest_data:
        u = (h.get('url') or '').strip().lower().rstrip('/')
        if u: h_by_url[u] = h
        nm = (h.get('name') or (h.get('first_name','') + ' ' + h.get('last_name',''))).strip().lower()
        co = (h.get('connected_on') or '').strip().lower()
        if nm and co: h_by_comp[(nm, co)] = h

    connections_rows = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        for fname in z.namelist():
            if fname.endswith('Connections.csv'):
                with z.open(fname) as f:
                    lines = f.read().decode('utf-8-sig', errors='ignore').splitlines()
                    reader = csv.reader([l for l in lines if l.strip()])
                    r_list = list(reader)
                    start = 0
                    for idx, r in enumerate(r_list):
                        if len(r) > 2 and 'First Name' in r[0]:
                            start = idx
                            break
                    connections_rows = r_list[start+1:]

    unified_contacts = []
    harvest_injected_count = 0
    job_movement_count = 0

    for r in connections_rows:
        fn = r[0].strip() if len(r) > 0 else ''
        ln = r[1].strip() if len(r) > 1 else ''
        url = r[2].strip() if len(r) > 2 else ''
        email = r[3].strip() if len(r) > 3 else ''
        company = r[4].strip() if len(r) > 4 else ''
        position = r[5].strip() if len(r) > 5 else ''
        connected_on = r[6].strip() if len(r) > 6 else ''
        name = f"{fn} {ln}".strip()
        if not name: continue

        c_id = generate_contact_id(vault_id, url, name, connected_on)
        u_clean = url.strip().lower().rstrip('/')
        h_match = h_by_url.get(u_clean) or h_by_comp.get((name.lower(), connected_on.lower()))

        country = infer_country(email, company, position)
        city = "Desconocido"
        lat = COUNTRY_COORDS.get(country, {}).get("lat", 19.4326)
        lng = COUNTRY_COORDS.get(country, {}).get("lng", -99.1332)
        audit_status = "unverified"
        job_status = "Vigente Probable"
        harvest_enriched = False
        metadata = {}

        if h_match:
            harvest_injected_count += 1
            harvest_enriched = True
            audit_status = "verified"
            country = h_match.get('country') or country
            city = h_match.get('city') or city
            lat = h_match.get('lat') or lat
            lng = h_match.get('lng') or lng
            
            h_comp = (h_match.get('company') or '').strip().lower()
            zip_comp = company.strip().lower()
            if zip_comp and h_comp and zip_comp != h_comp:
                job_movement_count += 1
                job_status = "🔄 Movimiento Laboral 2026"
                metadata['previous_company'] = h_match.get('company')
                metadata['previous_position'] = h_match.get('position')
                metadata['job_movement_alert'] = True
            else:
                company = h_match.get('company') or company
                position = h_match.get('position') or position
                job_status = "🟢 Vigente 2026 (Auditado)"

        unified_contacts.append({
            "id": c_id,
            "vault_id": vault_id,
            "name": name,
            "first_name": fn,
            "last_name": ln,
            "company": company,
            "position": position,
            "country": country,
            "city": city,
            "url": url,
            "email": email,
            "score": 75 if harvest_enriched else 50,
            "crm_status": "Ninguno",
            "audit_status": audit_status,
            "job_status": job_status,
            "metadata": {
                **metadata,
                "city": city,
                "country": country,
                "lat": lat,
                "lng": lng,
                "harvest_enriched": harvest_enriched,
                "connected_on": connected_on,
                "hierarchy": infer_hierarchy(position),
                "sector": infer_sector(position, company)
            }
        })

    print(f"✅ Total contactos procesados: {len(unified_contacts)}")
    print(f"💎 Contactos con Harvest inyectado: {harvest_injected_count}")
    print(f"🔄 Movimientos laborales detectados: {job_movement_count}")
    return unified_contacts

def wipe_vault_antonio():
    print("🧹 Vaciando vault_antonio en Supabase...")
    url = f"{SUPABASE_URL}/rest/v1/contacts?vault_id=eq.vault_antonio"
    req = urllib.request.Request(url, headers=headers, method='DELETE')
    try:
        with urllib.request.urlopen(req) as resp:
            print("✅ vault_antonio vaciado exitosamente en Supabase.")
            return True
    except Exception as e:
        print(f"❌ Error al vaciar vault_antonio: {e}")
        return False

def upload_in_chunks(contacts, chunk_size=200):
    total = len(contacts)
    print(f"🚀 Subiendo {total} contactos limpios a Supabase en lotes de {chunk_size}...")
    for i in range(0, total, chunk_size):
        chunk = contacts[i:i + chunk_size]
        url = f"{SUPABASE_URL}/rest/v1/contacts"
        data_bytes = json.dumps(chunk, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as resp:
                print(f" -> Lote {i//chunk_size + 1}/{(total + chunk_size - 1)//chunk_size} subido ({len(chunk)} contactos).")
        except Exception as e:
            print(f"❌ Error subiendo lote {i}: {e}")
            return False
    print("🎉 ¡CARGA MAESTRA COMPLETADA AL 100% EN SUPABASE!")
    return True

print("=== MOTOR RE-SEED MAESTRO LISTO PARA EJECUTARSE ===")
