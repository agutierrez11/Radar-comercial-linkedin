import json
import csv

with open('locations_normalized.json', 'r', encoding='utf-8') as f:
    locs = json.load(f)

ca_countries = ['Panamá', 'Panama', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Belice', 'Belize']
target_keys = []
for k, v in locs.items():
    if v.get('country') in ca_countries or v.get('country', '').lower() in [c.lower() for c in ca_countries]:
        target_keys.append(k)

print('Found CA keys in locations_normalized:', len(target_keys))
for k in target_keys:
    print(' -', k, '->', locs[k].get('country'))

with open('Connections.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    connections = list(reader)

found_people = []
for row in connections:
    comp = row.get('Company', '').strip()
    pos = row.get('Position', '').strip()
    key = f'{comp} | {pos}'
    if key in target_keys:
        found_people.append(row)

print('\nPeople in CA:')
for p in found_people:
    print(f"- {p['First Name']} {p['Last Name']} : {p['Position']} @ {p['Company']}")

