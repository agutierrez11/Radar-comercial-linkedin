import os
import json
import sys
from dotenv import load_dotenv
from supabase import create_client

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()
sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

# Traer perfiles procesados por HarvestAPI
offset = 0
PAGE = 500
harvest_rows = []

while True:
    r = sb.table("connections").select("*").range(offset, offset + PAGE - 1).execute()
    batch = r.data or []
    if not batch:
        break
    for row in batch:
        meta = row.get("metadata") or {}
        if meta.get("harvest_enriched"):
            harvest_rows.append(row)
    if len(batch) < PAGE:
        break
    offset += PAGE

print("=" * 60)
print(f"📊 AUDITORIA DE HARVESTAPI (TOTAL ENRIQUECIDOS HOY: {len(harvest_rows)})")
print("=" * 60)

with_country = [r for r in harvest_rows if (r.get("metadata") or {}).get("country")]
with_company = [r for r in harvest_rows if (r.get("metadata") or {}).get("harvest_company")]
with_city = [r for r in harvest_rows if (r.get("metadata") or {}).get("city")]

print(f"✅ Con país exacto:    {len(with_country)} / {len(harvest_rows)}")
print(f"✅ Con ciudad exacta:  {len(with_city)} / {len(harvest_rows)}")
print(f"✅ Con empresa actual: {len(with_company)} / {len(harvest_rows)}")
print("-" * 60)
print("Muestra aleatoria de 15 perfiles procesados hoy con HarvestAPI:")
print("-" * 60)

import random
sample = random.sample(harvest_rows, min(15, len(harvest_rows))) if harvest_rows else []

for i, r in enumerate(sample, 1):
    meta = r.get("metadata") or {}
    fn = r.get("first_name", "")
    ln = r.get("last_name", "")
    country = meta.get("country", "N/D")
    city = meta.get("city", "N/D")
    company = meta.get("harvest_company", "N/D")
    position = meta.get("harvest_position", "N/D")
    url = r.get("linkedin_url", "")
    print(f"{i:2d}. {fn} {ln}")
    print(f"    📍 {city}, {country}")
    print(f"    💼 {position} @ {company}")
    print(f"    🔗 {url}\n")

print("=" * 60)
