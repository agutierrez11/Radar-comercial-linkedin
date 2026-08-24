import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Print hierarchy around main container and section definitions
lines = html.splitlines()

print("--- SECTIONS FOUND ---")
for i, line in enumerate(lines, start=1):
    if 'id="sec-' in line or 'class="section' in line:
        print(f"Line {i}: {line.strip()[:120]}")
