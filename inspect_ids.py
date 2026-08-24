import json

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, c in enumerate(data):
    name = c.get('name') or c.get('full_name') or (c.get('first_name','') + ' ' + c.get('last_name',''))
    if 'estefany' in name.lower() or 'nicolau' in name.lower() or 'anurag' in name.lower():
        print(f"Name: '{name}', url: '{c.get('url')}', company: '{c.get('company')}'")
