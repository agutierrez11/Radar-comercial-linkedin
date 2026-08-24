import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

depth = 0
for i in range(977, 1815):
    line = lines[i]
    opens = len(re.findall(r'<div[\s>]', line))
    closes = len(re.findall(r'</div>', line))
    depth += (opens - closes)
    if 'id="sec-' in line or depth < 0:
        print(f"Line {i+1}: depth={depth} | {line.strip()[:90]}")
