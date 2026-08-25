import json

with open('master_data.json', 'r', encoding='utf-8', errors='replace') as f:
    d = json.load(f)

print("master_data.json ownerName:", d.get('ownerName'))
contacts = d.get('contacts', [])
print("Total contacts in master_data.json:", len(contacts))

discards = sum(1 for c in contacts if c.get('crmStatus') in ['Descartado', 'Archivado'] or c.get('discardedFromPurge'))
white = sum(1 for c in contacts if c.get('crmStatus') in ['Conservado', 'Protegido'] or c.get('whitelistedFromPurge'))
harvest = sum(1 for c in contacts if c.get('harvest_enriched') or c.get('isHarvestEnriched'))

print(f"Discards in master_data.json: {discards}")
print(f"Whitelisted in master_data.json: {white}")
print(f"Harvest Enriched in master_data.json: {harvest}")

if len(contacts) > 0:
    print("Sample contact 0:", contacts[0].get('name'), "| crmStatus:", contacts[0].get('crmStatus'))
