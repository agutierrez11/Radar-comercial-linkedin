import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:3000]):
    if 'const S =' in line or 'var S =' in line or 'let S =' in line:
        print(f"Line {i+1}: {line.strip()}")
