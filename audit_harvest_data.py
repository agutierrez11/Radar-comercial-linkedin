import urllib.request
import json
import os
import sys
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

print("=== AUDITANDO Y EXRAYENDO TODOS LOS PERFILES ENRIQUECIDOS EN SUPABASE ===")

all_contacts = []
offset = 0
limit = 1000

while True:
    url = f"{SUPABASE_URL}/rest/v1/contacts?select=*&vault_id=eq.vault_antonio&limit={limit}&offset={offset}"
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req) as resp:
            chunk = json.loads(resp.read().decode('utf-8'))
            if not chunk:
                break
            all_contacts.extend(chunk)
            print(f"Descargados {len(chunk)} contactos (Total acumulado: {len(all_contacts)})...")
            if len(chunk) < limit:
                break
            offset += limit
    except Exception as e:
        print(f"Error en chunk offset {offset}: {e}")
        break

print(f"\nTotal contactos obtenidos para vault_antonio: {len(all_contacts)}")

harvest_list = []
for c in all_contacts:
    meta = c.get('metadata') or {}
    if meta.get('harvest_enriched') or 'harvest' in str(meta).lower() or c.get('audit_status') == 'verified' or c.get('job_status') == 'Vigente 2026':
        harvest_list.append(c)

print(f"Total perfiles con enriquecimiento activo (Harvest / Verified / Vigente 2026): {len(harvest_list)}")

# Guardar backup completo de Antonio
with open("antonio_supabase_all_contacts_backup.json", "w", encoding="utf-8") as f_all:
    json.dump(all_contacts, f_all, ensure_ascii=False, indent=2)

# Guardar archivo exclusivo de los enriquecidos
with open("antonio_harvest_enriched_backup.json", "w", encoding="utf-8") as f_h:
    json.dump(harvest_list, f_h, ensure_ascii=False, indent=2)

print("\nARCHIVOS DE SEGURIDAD GENERADOS:")
print(f" 1. antonio_supabase_all_contacts_backup.json ({len(all_contacts)} contactos totales de tu bóveda en Supabase)")
print(f" 2. antonio_harvest_enriched_backup.json ({len(harvest_list)} perfiles enriquecidos)")

if harvest_list:
    h0 = harvest_list[0]
    print(f"\nEjemplo de perfil enriquecido:")
    print(f" - Nombre: {h0.get('name')}")
    print(f" - Empresa: {h0.get('company')}")
    print(f" - Puesto: {h0.get('position')}")
    print(f" - Estatus: {h0.get('job_status')} | Audit: {h0.get('audit_status')}")
    print(f" - Metadata: {h0.get('metadata')}")
