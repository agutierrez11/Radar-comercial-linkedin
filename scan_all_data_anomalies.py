import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 70)
print("🔍 ESCÁNER DE ANOMALÍAS EN TODA LA BASE DE DATOS (3,039 CONTACTOS)")
print("=" * 70)

# Cargar dataset
with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    contacts = json.load(f)

print(f"Total contactos cargados: {len(contacts)}\n")

anomalies = []

# Criterios de detección de basura
for c in contacts:
    reasons = []

    pos = str(c.get('position', ''))
    pos_curr = str(c.get('position_current', ''))
    comp = str(c.get('company', ''))
    country = str(c.get('country', ''))
    city = str(c.get('city', ''))
    url = str(c.get('url', ''))

    # 1. Cargo contiene texto de seguidores/contactos de LinkedIn
    if re.search(r'\b(followers?|seguidores?|contactos?|connections?)\b', pos_curr, re.I) or \
       re.search(r'\b(followers?|seguidores?|contactos?|connections?)\b', pos, re.I):
        reasons.append("Cargo contiene texto de seguidores ('followers/contactos')")

    # 2. País = Argentina pero la empresa o cargo menciona México, CDMX, Colombia, Chile, etc.
    if country == 'Argentina':
        full_text = (pos + ' ' + pos_curr + ' ' + comp + ' ' + url).lower()
        if any(kw in full_text for kw in ['mexico', 'méxico', 'cdmx', 'colombia', 'chile', 'peru', 'perú', 'monterrey', 'guadalajara']):
            reasons.append("País asignado 'Argentina' pero texto menciona México/LATAM")

    # 3. Cargo vacío o solo números
    if pos_curr.strip().isdigit():
        reasons.append(f"Cargo actual es solo un número: '{pos_curr}'")

    if reasons:
        anomalies.append({
            'id': c.get('id'),
            'name': c.get('full_name') or f"{c.get('first_name','')} {c.get('last_name','')}".strip(),
            'company': comp,
            'position_zip': pos,
            'position_curr': pos_curr,
            'country': country,
            'reasons': reasons
        })

print(f"⚠️ ANOMALÍAS DETECTADAS EN TOTAL: {len(anomalies)} / {len(contacts)}")
print("=" * 70)

for i, a in enumerate(anomalies, 1):
    print(f"{i:2d}. {a['name']} | Empresa: {a['company']}")
    print(f"    Cargo ZIP: {a['position_zip']}")
    print(f"    Cargo Current: {a['position_curr']}")
    print(f"    País: {a['country']}")
    print(f"    🚨 Problema: {', '.join(a['reasons'])}\n")

print("=" * 70)
