import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if 'gisMap' in line:
        print(f"Line {i}: {line.strip()[:100]}")
