import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

kws = ['guatemala', 'salvador', 'honduras', 'nicaragua', 'costa rica', 'panama', 'panamá', 'el salvador', 'tegucigalpa', 'managua', 'san josé', 'san jose']
found = []

for c in data:
    txt = json.dumps(c, ensure_ascii=False).lower()
    if any(k in txt for k in kws):
        found.append(c)

print(f"Total contactos con menciones de CA en dataset: {len(found)}")
print("=" * 70)

for i, c in enumerate(found, 1):
    name = c.get('full_name') or f"{c.get('first_name','')} {c.get('last_name','')}"
    country = c.get('country')
    city = c.get('city')
    pos = c.get('position')
    pos_curr = c.get('position_current')
    comp = c.get('company')
    meta = c.get('metadata') or {}
    print(f"{i:2d}. {name}")
    print(f"    📍 País: {country} | Ciudad: {city}")
    print(f"    💼 Cargo: {pos} (Actual: {pos_curr}) @ {comp}")
    print(f"    🔗 {c.get('url')}\n")
