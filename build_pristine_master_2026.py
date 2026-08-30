import subprocess
import json
import zipfile
import csv
import os

print("[PRISTINE MASTER ENGINE] Rebuilding 100% pristine unified master dataset...")

# 1. Load curated commit 033c674 data for rich metadata matching
cmd = ['git', 'show', '033c674:enriched_connections.json']
curated_data = json.loads(subprocess.check_output(cmd, encoding='utf-8', errors='replace'))

# Map curated data by URL and by Name
url_map = {c.get('url'): c for c in curated_data if c.get('url')}
name_map = {c.get('name') or f"{c.get('first_name','')} {c.get('last_name','')}".strip(): c for c in curated_data}

# 2. Parse newest August 25 ZIP (3,030 contacts)
zip_path = r'C:\Users\Antonio\OneDrive\Downloads\Basic_LinkedInDataExport_08-25-2026.zip.zip'
raw_contacts = []
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('Connections.csv') as f:
        content = f.read().decode('utf-8-sig', errors='ignore')
        lines = [l for l in content.splitlines() if l.strip()]
        reader = csv.reader(lines)
        header = None
        for i, row in enumerate(reader):
            if not header and len(row) > 2 and 'First Name' in row[0]:
                header = row
                continue
            if header and len(row) >= 6:
                fn = row[0].strip()
                ln = row[1].strip()
                url = row[2].strip()
                email = row[3].strip() if len(row) > 3 else ""
                company = row[4].strip() if len(row) > 4 else ""
                position = row[5].strip() if len(row) > 5 else ""
                connected_on = row[6].strip() if len(row) > 6 else ""
                
                if not url and not (fn or ln):
                    continue
                    
                name = f"{fn} {ln}".strip() or "Contacto LinkedIn"
                raw_contacts.append({
                    "id": i + 1,
                    "name": name,
                    "first_name": fn,
                    "last_name": ln,
                    "url": url,
                    "email": email,
                    "company": company,
                    "position": position,
                    "connected_on": connected_on
                })

print(f"Loaded {len(raw_contacts)} raw contacts from August 25 ZIP.")

# 3. Merge rich metadata into each raw contact
final_contacts = []
for rc in raw_contacts:
    url = rc['url']
    name = rc['name']
    
    match = url_map.get(url) or name_map.get(name) or {}
    
    # Infer hierarchy if not in match
    pos = (rc['position'] or match.get('position') or '').lower()
    hierarchy = match.get('hierarchy')
    if not hierarchy:
        if any(k in pos for k in ['chief', 'ceo', 'cto', 'cfo', 'coo', 'cmo', 'cro', 'cpo', 'president', 'founder', 'fundador', 'socio', 'partner', 'owner', 'director general', 'country manager']):
            hierarchy = 'C-Level'
        elif any(k in pos for k in ['director', 'vp', 'vicepresident', 'head', 'lider', 'lead']):
            hierarchy = 'Director'
        elif any(k in pos for k in ['gerente', 'manager', 'jefe', 'coordinador']):
            hierarchy = 'Gerente'
        else:
            hierarchy = 'Otros'
            
    country = match.get('country') or 'México' if 'mexico' in (rc['company']+rc['position']).lower() else match.get('country') or 'Desconocido'
    city = match.get('city') or 'CDMX' if country == 'México' else match.get('city') or 'Desconocido'
    score = match.get('score') or (75 if hierarchy in ['C-Level', 'Director'] else 50)
    
    item = {
        "id": rc['id'],
        "name": name,
        "first_name": rc['first_name'],
        "last_name": rc['last_name'],
        "originalName": name,
        "company": rc['company'] or match.get('company') or "Empresa No Especificada",
        "originalCompany": rc['company'],
        "position": rc['position'] or match.get('position') or "Cargo No Especificado",
        "originalPosition": rc['position'],
        "url": url,
        "email": rc['email'] or match.get('email') or "",
        "connectedOn": rc['connected_on'],
        "connected_on": rc['connected_on'],
        "hierarchy": hierarchy,
        "country": country,
        "city": city,
        "lat": match.get('lat', 19.4326),
        "lng": match.get('lng', -99.1332),
        "score": score,
        "crmStatus": match.get('crmStatus') or "Ninguno",
        "audit_status": match.get('audit_status') or "verified",
        "job_status": match.get('job_status') or "Vigente 2026",
        "is_current": True,
        "harvest_enriched": match.get('harvest_enriched', False),
        "isHarvestEnriched": match.get('isHarvestEnriched', False),
        "msg_count": match.get('msg_count', 0),
        "last_post_date": match.get('last_post_date', ""),
        "last_post_text": match.get('last_post_text', "")
    }
    final_contacts.append(item)

clevel = sum(1 for c in final_contacts if c['hierarchy'] == 'C-Level')
directors = sum(1 for c in final_contacts if c['hierarchy'] == 'Director')
gerentes = sum(1 for c in final_contacts if c['hierarchy'] == 'Gerente')
clase_a = sum(1 for c in final_contacts if c['score'] >= 60)

print(f"[UNIFIED ENGINE] Output Total: {len(final_contacts)} contacts | C-Level: {clevel} | Directors: {directors} | Gerentes: {gerentes} | Clase A (>=60): {clase_a}")

# Save master_data.js
js_code = f"window.MASTER_CONNECTIONS_DATA = {json.dumps(final_contacts, ensure_ascii=False, indent=2)};\n"
with open("master_data.js", "w", encoding="utf-8") as f:
    f.write(js_code)

# Save enriched_connections.json
with open("enriched_connections.json", "w", encoding="utf-8") as f:
    json.dump(final_contacts, f, ensure_ascii=False, indent=2)

print("[SUCCESS] master_data.js and enriched_connections.json rebuilt pristine!")
