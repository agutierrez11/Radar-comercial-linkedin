import json
import os
import re
import sys
from dotenv import load_dotenv
from supabase import create_client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

print("=" * 70)
print("🧹 REPARACIÓN DETERMINÍSTICA DE 441 ANOMALÍAS EN TODA LA BASE")
print("=" * 70)

# Cargar dataset local
with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    contacts = json.load(f)

fixed_count = 0

for c in contacts:
    meta = c.get('metadata') or {}
    
    # Solo tocar si NO ha sido enriquecido por HarvestAPI hoy (HarvestAPI es la fuente primaria 100% limpia)
    if meta.get('harvest_enriched'):
        continue

    pos = str(c.get('position', ''))
    pos_curr = str(c.get('position_current', ''))
    comp = str(c.get('company', ''))
    country = str(c.get('country', ''))

    was_fixed = False

    # Fix 1: Cargo con texto basura de seguidores -> restaurar con el cargo original de Connections.csv (position_zip)
    if re.search(r'\b(followers?|seguidores?|contactos?|connections?)\b', pos_curr, re.I) or pos_curr.strip().isdigit():
        clean_pos = pos if pos and not re.search(r'\b(followers?|seguidores?|contactos?)\b', pos, re.I) else comp
        c['position_current'] = clean_pos
        c['position'] = clean_pos
        c['job_status'] = "🟢 Vigente ZIP"
        c['audit_status'] = "Activo Auditado"
        was_fixed = True

    # Fix 2: Argentina erróneo en perfiles que mencionan México/LATAM
    if country == 'Argentina':
        full_text = (pos + ' ' + pos_curr + ' ' + comp + ' ' + str(c.get('url',''))).lower()
        if any(kw in full_text for kw in ['mexico', 'méxico', 'cdmx', 'colombia', 'chile', 'peru', 'perú', 'monterrey', 'guadalajara']):
            c['country'] = 'México' if 'mexico' in full_text or 'cdmx' in full_text else 'LATAM'
            c['city'] = 'CDMX' if 'cdmx' in full_text or 'mexico city' in full_text else 'Desconocido'
            was_fixed = True

    if was_fixed:
        fixed_count += 1

print(f"✅ Se repararon {fixed_count} registros en enriched_connections.json.")

# Guardar JSON reparado
with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(contacts, f, indent=2, ensure_ascii=False)

print("[INFO] Guardado en enriched_connections.json.")

# Ahora sincronizar los arreglos en Supabase
print("[INFO] Sincronizando reparaciones en Supabase...")

offset = 0
PAGE = 500
supa_updated = 0

while True:
    res = sb.table("connections").select("id, linkedin_url, current_position, current_company, metadata").range(offset, offset + PAGE - 1).execute()
    batch = res.data or []
    if not batch:
        break
    
    for row in batch:
        m = row.get("metadata") or {}
        if m.get("harvest_enriched"):
            continue
            
        cur_pos = str(row.get("current_position", ""))
        row_id = row.get("id")
        
        if re.search(r'\b(followers?|seguidores?|contactos?|connections?)\b', cur_pos, re.I) or cur_pos.strip().isdigit() or m.get("job_status") == "🟡 Drift Detectado (Posible Cambio de Empresa)":
            # Buscar coincidencia en contactos locales por URL
            url = row.get("linkedin_url", "")
            match = next((x for x in contacts if x.get("url") == url), None)
            
            clean_p = match.get("position") if match else (row.get("current_company") or "Ejecutivo")
            clean_country = match.get("country") if match else "Desconocido"
            
            m["job_status"] = "🟢 Vigente ZIP"
            m["audit_status"] = "Activo Auditado"
            if clean_country != "Desconocido":
                m["country"] = clean_country

            sb.table("connections").update({
                "current_position": clean_p,
                "metadata": m
            }).eq("id", row_id).execute()
            
            supa_updated += 1

    if len(batch) < PAGE:
        break
    offset += PAGE

print(f"✅ Supabase actualizado: {supa_updated} registros reparados.")
print("=" * 70)
