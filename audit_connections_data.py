import json

with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    data = json.load(f)

print(f"Total contacts in enriched_connections.json: {len(data)}")

discarded = [c for c in data if c.get('crmStatus') == 'Descartado' or c.get('discardedFromPurge')]
whitelisted = [c for c in data if c.get('crmStatus') == 'Conservado' or c.get('whitelistedFromPurge') or c.get('crmStatus') == 'Protegido']
harvest = [c for c in data if c.get('harvest_enriched')]

print(f"Discarded: {len(discarded)}")
print(f"Whitelisted: {len(whitelisted)}")
print(f"Harvest Enriched: {len(harvest)}")

# Check sample names and positions
print("\nSample contacts:")
for c in data[:5]:
    name = c.get('name') or (c.get('first_name', '') + ' ' + c.get('last_name', '')).strip()
    pos = c.get('position') or c.get('position_current', '')
    company = c.get('company') or c.get('company_zip', '')
    country = c.get('country', '')
    print(f"- {name} | {pos} @ {company} | {country}")
