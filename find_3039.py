import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if '3039' in line or '3,039' in line:
        print(f"Line {i}: {line.strip()[:100]}")
