import os
import json
import sys
from dotenv import load_dotenv
from supabase import create_client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

print("=" * 70)
print("🧹 DEDUPLICACIÓN DE FILAS EN SUPABASE ( connections )")
print("=" * 70)

# Descargar todas las conexiones con su ID y linkedin_url
print("Descargando registros...")
offset = 0
PAGE = 1000
all_records = []
while True:
    res = sb.table("connections").select("id, linkedin_url, metadata").range(offset, offset + PAGE - 1).execute()
    batch = res.data or []
    all_records.extend(batch)
    if len(batch) < PAGE:
        break
    offset += PAGE

print(f"Total registros en Supabase: {len(all_records)}")

# Agrupar por URL
url_map = {}
for r in all_records:
    url = (r.get("linkedin_url") or "").rstrip("/").strip()
    if not url:
        continue
    if url not in url_map:
        url_map[url] = []
    url_map[url].append(r)

to_delete_ids = []
kept_count = 0

for url, group in url_map.items():
    if len(group) == 1:
        kept_count += 1
        continue
    
    # Si hay duplicados, elegir el mejor para conservar:
    # Priorizar el que tenga metadata con harvest_enriched = True
    sorted_group = sorted(
        group,
        key=lambda x: (
            (x.get("metadata") or {}).get("harvest_enriched", False) is True,
            len(json.dumps(x.get("metadata") or {}))
        ),
        reverse=True
    )
    
    # El primero se queda
    kept = sorted_group[0]
    kept_count += 1
    
    # Los demás se eliminan
    for dupe in sorted_group[1:]:
        to_delete_ids.append(dupe["id"])

print(f"Registros únicos que se conservarán: {kept_count}")
print(f"Duplicados a eliminar: {len(to_delete_ids)}")

if to_delete_ids:
    print("Eliminando duplicados de Supabase...")
    # Eliminar en lotes de 100
    chunk_size = 100
    deleted_count = 0
    for i in range(0, len(to_delete_ids), chunk_size):
        chunk = to_delete_ids[i:i+chunk_size]
        res = sb.table("connections").delete().in_("id", chunk).execute()
        deleted_count += len(chunk)
        print(f"  Eliminados {deleted_count}/{len(to_delete_ids)}...")
    print("✅ Deduplicación en base de datos completada.")
else:
    print("✅ No hay duplicados en Supabase.")
print("=" * 70)
