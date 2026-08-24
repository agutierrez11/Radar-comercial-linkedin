import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'\.section[\{\s\S]*?\}', content)
for m in matches[:10]:
    print(m[:300])
    print("---")
