import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

search_roots = [
    r"c:\Users\Antonio\.gemini\antigravity-ide\scratch",
    r"c:\Users\Antonio\.gemini\antigravity-ide\brain",
    r"c:\Users\Antonio\.gemini",
    r"c:\Users\Antonio\Desktop"
]

found = []

for root_dir in search_roots:
    if not os.path.exists(root_dir):
        continue
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(('.py', '.json', '.env', '.md', '.txt', '.log', '.jsonl', '.js', '.ts', '.html')):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        if 'nvapi-' in content:
                            idx = content.find('nvapi-')
                            snippet = content[idx:idx+70]
                            found.append((filepath, snippet))
                except Exception:
                    pass

print(f"Búsqueda finalizada. Claves nvapi- encontradas: {len(found)}")
for path, snip in found:
    # Clean up non-printable
    snip_clean = "".join(c for c in snip if c.isalnum() or c in "-_")
    print(f"Archivo: {path}")
    print(f"  Snippet: {snip_clean[:15]}...{snip_clean[-5:]}")
