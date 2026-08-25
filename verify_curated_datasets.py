import json

# Check master_data.json
with open('master_data.json', 'r', encoding='utf-8', errors='replace') as f:
    master_dict = json.load(f)

contacts = master_dict.get('contacts', [])
print(f"master_data.json total contacts: {len(contacts)}")

# Check master_data.js
with open('master_data.js', 'r', encoding='utf-8', errors='replace') as f:
    js_content = f.read()

import re
m = re.search(r'window\.__MASTER_DATA__\s*=\s*(\[[\s\S]*\]);?', js_content)
if m:
    js_arr = json.loads(m.group(1))
    print(f"master_data.js total contacts: {len(js_arr)}")
else:
    print("master_data.js pattern not matched directly.")

# Check enriched_connections.json
with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    enriched_arr = json.load(f)
print(f"enriched_connections.json total contacts: {len(enriched_arr)}")
