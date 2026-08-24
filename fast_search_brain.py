import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

brain_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\brain"

found = []

if os.path.exists(brain_dir):
    for root, dirs, files in os.walk(brain_dir):
        for f in files:
            if f.endswith('.jsonl') or f.endswith('.txt') or f.endswith('.env') or f.endswith('.py') or f.endswith('.md'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        if 'nvapi-' in content:
                            idx = content.find('nvapi-')
                            snippet = content[idx:idx+80]
                            found.append((filepath, snippet))
                except Exception:
                    pass

print(f"Búsqueda finalizada en brain logs. Hallazgos: {len(found)}")
for p, s in found:
    clean_s = s.split()[0].split('"')[0].split("'")[0].split('\\n')[0]
    print(f"MATCH: {p}")
    print(f"KEY: {clean_s}")
