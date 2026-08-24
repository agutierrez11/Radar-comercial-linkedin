import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[8200:8450], start=8201):
    if 'quickLogin' in line or 'submitCustom' in line or 'openLogin' in line or 'setup' in line or 'Ronan' in line or 'Giovanna' in line:
        print(f"Line {i}: {line.strip()}")
