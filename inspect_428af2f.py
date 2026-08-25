import json, subprocess

cmd = ['git', 'show', '428af2f:master_data.json']
res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
d = json.loads(res)

contacts = d.get('contacts', [])
print("Total contacts in 428af2f master_data.json:", len(contacts))

for c in contacts[:10]:
    st = c.get('crmStatus') or c.get('status')
    disc = c.get('discardedFromPurge')
    white = c.get('whitelistedFromPurge')
    harv = c.get('harvest_enriched') or c.get('isHarvestEnriched')
    name = c.get('name') or c.get('first_name', '')
    print(f"Name: {name[:30]} | status: {st} | disc: {disc} | white: {white} | harv: {harv}")

# Count statuses
status_counts = {}
for c in contacts:
    st = c.get('crmStatus') or 'none'
    status_counts[st] = status_counts.get(st, 0) + 1

print("\nStatus counts in 428af2f master_data.json:", status_counts)
