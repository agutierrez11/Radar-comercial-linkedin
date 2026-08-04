import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

kws = ['guatemala', 'salvador', 'honduras', 'nicaragua', 'costa rica', 'panama', 'panamá', 'belice', 'belize']
found = []

for c in data:
    txt = (str(c.get('country','')) + ' ' + str(c.get('city','')) + ' ' + str(c.get('position','')) + ' ' + str(c.get('company',''))).lower()
    if any(k in txt for k in kws):
        found.append(c)

print(f"Total contactos de Centroamérica en dataset: {len(found)}")
print("=" * 60)

for i, c in enumerate(found, 1):
    name = c.get('full_name') or f"{c.get('first_name','')} {c.get('last_name','')}"
    country = c.get('country')
    city = c.get('city')
    pos = c.get('position')
    comp = c.get('company')
    print(f"{i:2d}. {name}")
    print(f"    📍 País: {country} | Ciudad: {city}")
    print(f"    💼 {pos} @ {comp}\n")
