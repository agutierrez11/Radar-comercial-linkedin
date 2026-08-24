import json

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

contacts = data if isinstance(data, list) else data.get('contacts', [])
messages = data.get('messages', []) if isinstance(data, dict) else []

print(f"Total contacts: {len(contacts)}, Total messages: {len(messages)}")

print("\n--- MATCHES IN CONTACT FIELDS ---")
for i, c in enumerate(contacts):
    txt = json.dumps(c, ensure_ascii=False).lower()
    if 'cubre' in txt or 'boca' in txt:
        name = c.get('name') or c.get('First Name', '') + ' ' + c.get('Last Name', '')
        pos = c.get('position') or c.get('Position', '')
        matching_keys = [k for k, v in c.items() if 'cubre' in str(v).lower() or 'boca' in str(v).lower()]
        print(f"Match #{i}: Name='{name}', Position='{pos}', Matching Keys={matching_keys}")
        for k in matching_keys:
            print(f"   -> {k}: {str(c[k])[:150]}")
