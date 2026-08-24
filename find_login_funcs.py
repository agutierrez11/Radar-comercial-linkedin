with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.finditer(r'(quickLogin|submitCustomLogin|openLoginModal|switchVault)', content)
for m in matches:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 300)
    print(f"Match at {m.start()}:")
    print(content[start:end])
    print("-" * 50)
