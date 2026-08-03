import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

they_selling = [c for c in data if c.get('is_they_selling')]
print(f"=== VERIFICACIÓN: {len(they_selling)} PERSONAS QUE INTENTARON VENDERTE A TI ===")
for c in they_selling[:5]:
    name = c.get('full_name') or (c.get('first_name','') + ' ' + c.get('last_name',''))
    pos = c.get('position') or '-'
    comp = c.get('company') or '-'
    snippet = (c.get('last_msg_snippet') or '').replace('\n', ' ')
    print(f"* {name} ({pos} @ {comp}):\n  Snippet: \"{snippet[:100]}...\"\n")

friendly = [c for c in data if c.get('is_friendly')]
print(f"\n=== VERIFICACIÓN: {len(friendly)} SALUDOS AMISTOSOS / SOCIALES ===")
for c in friendly[:5]:
    name = c.get('full_name') or (c.get('first_name','') + ' ' + c.get('last_name',''))
    pos = c.get('position') or '-'
    comp = c.get('company') or '-'
    snippet = (c.get('last_msg_snippet') or '').replace('\n', ' ')
    print(f"* {name} ({pos} @ {comp}):\n  Snippet: \"{snippet[:100]}...\"\n")
