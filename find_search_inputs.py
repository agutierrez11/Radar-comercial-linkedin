import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if 'input' in line.lower() and 'search' in line.lower():
        print(f"Line {i}: {line.strip()[:140]}")
