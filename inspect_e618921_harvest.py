import subprocess, json

cmd = ['git', 'show', 'e618921:enriched_connections.json']
res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
data_e61 = json.loads(res)

harvest_contacts = [c for c in data_e61 if c.get('harvest_enriched') or c.get('isHarvestEnriched') or (c.get('metadata') and c['metadata'].get('harvest_enriched'))]

print(f"Total contacts in commit e618921: {len(data_e61)}")
print(f"Total Harvest Enriched contacts in commit e618921: {len(harvest_contacts)}")

# Check sample names
for c in harvest_contacts[:10]:
    name = c.get('name') or (c.get('first_name', '') + ' ' + c.get('last_name', '')).strip()
    company = c.get('company') or c.get('current_company')
    pos = c.get('position') or c.get('current_position')
    country = c.get('country')
    print(f"- {name} | {pos} @ {company} | {country}")
