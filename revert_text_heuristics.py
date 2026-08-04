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
print("🛡️ REVERSIÓN DE INFERENCIAS DE TEXTO (SOLO HarvestAPI VERIFICADO)")
print("=" * 70)

with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    contacts = json.load(f)

reverted = 0

for c in contacts:
    meta = c.get('metadata') or {}
    # Si NO ha sido enriquecido por HarvestAPI en vivo, quitar el país inferido por texto para evitar falsos positivos
    if not meta.get('harvest_enriched'):
        if c.get('country') and c.get('job_status') == "🟢 Vigente ZIP (Ubicación Inferida)":
            c['country'] = "Desconocido"
            c['city'] = "Desconocido"
            c['job_status'] = "🟢 Vigente ZIP"
            reverted += 1

# Asegurar Yamil Bravo en Cancún, México
for c in contacts:
    if 'yamil' in (c.get('first_name') or '').lower() and 'bravo' in (c.get('last_name') or '').lower():
        c['country'] = 'México'
        c['city'] = 'Cancún'

print(f"✅ Se revirtieron {reverted} inferencias ambiguas por texto.")

with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(contacts, f, indent=2, ensure_ascii=False)

# Sincronizar Supabase
offset = 0
PAGE = 500
supa_clean = 0

while True:
    res = sb.table("connections").select("id, metadata").range(offset, offset + PAGE - 1).execute()
    batch = res.data or []
    if not batch:
        break
    for row in batch:
        m = row.get("metadata") or {}
        if not m.get("harvest_enriched") and m.get("job_status") == "🟢 Vigente ZIP (Ubicación Inferida)":
            m["country"] = "Desconocido"
            m["city"] = "Desconocido"
            m["job_status"] = "🟢 Vigente ZIP"
            sb.table("connections").update({"metadata": m}).eq("id", row["id"]).execute()
            supa_clean += 1

    if len(batch) < PAGE:
        break
    offset += PAGE

print(f"✅ Supabase restaurado: {supa_clean} registros ambiguos limpiados.")
print("=" * 70)
