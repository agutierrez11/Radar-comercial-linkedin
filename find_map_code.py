import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if 'map' in line.lower() and ('function' in line.lower() or 'button' in line.lower() or 'onclick' in line.lower() or 'id=' in line.lower()):
        if len(line.strip()) < 150:
            print(f"Line {i}: {line.strip()}")
