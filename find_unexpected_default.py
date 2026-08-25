import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'default' in line and ('}' in line or ';' in line or 'default' in line):
        print(f"Line {i+1}: {line.strip()}")
