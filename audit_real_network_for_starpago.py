import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("enriched_connections.json", "r", encoding="utf-8") as f:
    contacts = json.load(f)

print(f"📊 Auditando tu Red Real ({len(contacts)} contactos):")

companies = {}
c_levels = []
directors = []
sectors = {}

for c in contacts:
    comp = c.get("company", "")
    pos = c.get("position", "")
    name = c.get("full_name", "")
    hier = c.get("hierarchy", "")
    
    if comp and comp != "Empresa No Especificada":
        companies[comp] = companies.get(comp, 0) + 1
        
    if hier == "C-Level":
        c_levels.append(f"{name} ({pos} @ {comp})")
    elif hier == "Director":
        directors.append(f"{name} ({pos} @ {comp})")

print("\n🏢 Top 10 Empresas en tu Red Real:")
sorted_comp = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
for comp, count in sorted_comp:
    print(f"  • {comp}: {count} contactos de 1er grado")

print("\n👑 Muestra de Contactos C-Level en tu Red:")
for c in c_levels[:5]:
    print(f"  • {c}")

print("\n🎯 Muestra de Directores en tu Red:")
for d in directors[:5]:
    print(f"  • {d}")
