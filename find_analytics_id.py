import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    if 'analytics' in line.lower() or 'sec-' in line.lower():
        if '<section' in line or 'id=' in line or 'onclick="navigate' in line:
            print(f"Line {i}: {line.strip()[:120]}")
