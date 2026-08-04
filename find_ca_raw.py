import pandas as pd
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('Connections.csv', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

header_idx = 0
for i, l in enumerate(lines[:10]):
    if 'First Name' in l:
        header_idx = i
        break

df = pd.read_csv(io.StringIO(''.join(lines[header_idx:])))

kws = ['guatemala', 'salvador', 'honduras', 'nicaragua', 'costa rica', 'panama', 'panamá', 'belice', 'belize', 'centroamérica', 'centroamerica', 'caribe']

found = []
for idx, row in df.iterrows():
    text = (str(row.get('First Name','')) + ' ' + str(row.get('Last Name','')) + ' ' + str(row.get('Company','')) + ' ' + str(row.get('Position','')) + ' ' + str(row.get('URL',''))).lower()
    if any(k in text for k in kws):
        found.append(row)

print(f"Total contactos con referencias de Centroamérica en Connections.csv: {len(found)}")
print("=" * 70)
for r in found:
    print(f"👤 {r.get('First Name')} {r.get('Last Name')}")
    print(f"   💼 {r.get('Position')} @ {r.get('Company')}")
    print(f"   🔗 {r.get('URL')}\n")
