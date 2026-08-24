import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("master_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total registros en master_data.json: {len(data)}")
sample = data[0] if data else {}
print("Campos disponibles por contacto:")
for k, v in sample.items():
    print(f" - {k}: {str(v)[:60]}")

# Conteo de ICPs, enriquecidos, y paises
with_country = sum(1 for d in data if d.get("country") or d.get("Country"))
with_company = sum(1 for d in data if d.get("company") or d.get("Company"))
with_position = sum(1 for d in data if d.get("position") or d.get("Position"))
with_enrichment = sum(1 for d in data if d.get("enriched") or d.get("apify_enriched") or d.get("summary"))

print(f"\nResumen de Calidad:")
print(f" - Con Empresa: {with_company} / {len(data)}")
print(f" - Con Cargo: {with_position} / {len(data)}")
print(f" - Con País/Ubicación: {with_country} / {len(data)}")
