import json
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

print("=" * 70)
print("🌎 INFERENCIA Y ASIGNACIÓN DE UBICACIONES PARA CENTROAMÉRICA Y CARIBE")
print("=" * 70)

with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    contacts = json.load(f)

ca_rules = [
    {'kw': 'honduras', 'country': 'Honduras', 'city': 'Tegucigalpa'},
    {'kw': 'guatemala', 'country': 'Guatemala', 'city': 'Ciudad de Guatemala'},
    {'kw': 'costa rica', 'country': 'Costa Rica', 'city': 'San José'},
    {'kw': 'fifco', 'country': 'Costa Rica', 'city': 'San José'},
    {'kw': 'panama', 'country': 'Panamá', 'city': 'Ciudad de Panamá'},
    {'kw': 'panamá', 'country': 'Panamá', 'city': 'Ciudad de Panamá'},
    {'kw': 'nicaragua', 'country': 'Nicaragua', 'city': 'Managua'},
    {'kw': 'el salvador', 'country': 'El Salvador', 'city': 'San Salvador'},
    {'kw': 'salvador', 'country': 'El Salvador', 'city': 'San Salvador'},
    {'kw': 'dominican republic', 'country': 'República Dominicana', 'city': 'Santo Domingo'},
    {'kw': 'república dominicana', 'country': 'República Dominicana', 'city': 'Santo Domingo'},
    {'kw': 'puerto rico', 'country': 'Puerto Rico', 'city': 'San Juan'},
    {'kw': 'belice', 'country': 'Belice', 'city': 'Belmopán'},
    {'kw': 'belize', 'country': 'Belice', 'city': 'Belmopán'},
    {'kw': 'centroamérica', 'country': 'Costa Rica', 'city': 'San José'},
    {'kw': 'centroamerica', 'country': 'Costa Rica', 'city': 'San José'},
]

fixed_count = 0

for c in contacts:
    # Si ya fue enriquecido por HarvestAPI hoy, no sobreescribir
    meta = c.get('metadata') or {}
    if meta.get('harvest_enriched') and c.get('country'):
        continue

    text = (str(c.get('company','')) + ' ' + str(c.get('position','')) + ' ' + str(c.get('position_current',''))).lower()

    # Evitar falsos positivos como "salvador" en nombres
    name_str = (str(c.get('first_name','')) + ' ' + str(c.get('last_name',''))).lower()
    
    for r in ca_rules:
        kw = r['kw']
        if kw in text and (kw != 'salvador' or 'el salvador' in text or 'salvador' in str(c.get('company','')).lower()):
            c['country'] = r['country']
            c['city'] = r['city']
            c['job_status'] = "🟢 Vigente ZIP (Ubicación Inferida)"
            fixed_count += 1
            print(f"✅ {c.get('full_name')} -> {r['country']} ({r['city']})")
            break

print(f"\n[INFO] Asignadas ubicaciones a {fixed_count} contactos de Centroamérica.")

with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(contacts, f, indent=2, ensure_ascii=False)

# Actualizar Supabase
print("[INFO] Actualizando Supabase para Centroamérica...")
supa_updated = 0

for c in contacts:
    if c.get('country') in ['Honduras', 'Guatemala', 'Costa Rica', 'Panamá', 'Panama', 'Nicaragua', 'El Salvador', 'República Dominicana', 'Puerto Rico', 'Belice']:
        url = c.get('url', '')
        if not url:
            continue
        res = sb.table('connections').select('id, metadata').eq('linkedin_url', url).execute()
        for row in (res.data or []):
            m = row.get('metadata') or {}
            m['country'] = c['country']
            m['city'] = c['city']
            m['job_status'] = c['job_status']
            sb.table('connections').update({
                'metadata': m
            }).eq('id', row['id']).execute()
            supa_updated += 1

print(f"✅ Supabase actualizado: {supa_updated} registros de Centroamérica sincronizados.")
print("=" * 70)
