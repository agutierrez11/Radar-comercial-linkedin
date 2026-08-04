import json

try:
    with open('enriched_connections.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f'Error loading json: {e}')
    data = []

countries = ['Panamá', 'Panama', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Belice', 'Belize']
keywords = ['pago', 'payment', 'pay', 'fintech', 'wallet', 'tarjeta', 'card', 'banco', 'bank', 'remesa', 'adquirente', 'adquiriente', 'visa', 'mastercard', 'stripe', 'dlocal', 'kushki']

results = []
for p in data:
    loc = p.get('Location', '') or ''
    if not isinstance(loc, str):
        continue
    loc_lower = loc.lower()
    in_target_country = any(c.lower() in loc_lower for c in countries)
    
    if in_target_country:
        title = p.get('Position', '') or p.get('Title', '') or ''
        company = p.get('Company', '') or ''
        industry = p.get('Industry', '') or ''
        
        text_to_search = f'{title} {company} {industry}'.lower()
        if any(k in text_to_search for k in keywords):
            name = p.get('FirstName', '') + ' ' + p.get('LastName', '')
            if not name.strip():
                name = p.get('Name', 'Unknown')
            results.append({
                'Name': name,
                'Position': title,
                'Company': company,
                'Location': loc
            })

for r in results:
    print(f"- {r['Name']}: {r['Position']} en {r['Company']} ({r['Location']})")
print(f'Total: {len(results)}')
