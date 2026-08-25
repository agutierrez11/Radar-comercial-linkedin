import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'clear' in line.lower() or 'reset' in line.lower() or 'vaciar' in line.lower() or 'purge' in line.lower():
        if 'function' in line:
            print(f"Line {i+1}: {line.strip()}")
