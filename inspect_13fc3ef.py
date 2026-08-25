import subprocess, json

cmd = ['git', 'show', '13fc3ef:enriched_connections.json']
res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
data = json.loads(res)

print("--- Commit 13fc3ef:enriched_connections.json ---")
print("Total contacts:", len(data))

# Breakdown of CRM status
status_map = {}
for c in data:
    st = c.get('crmStatus') or 'Ninguno'
    status_map[st] = status_map.get(st, 0) + 1

print("CRM Statuses:", status_map)

# Harvest enriched
harvest_count = sum(1 for c in data if c.get('harvest_enriched') or c.get('isHarvestEnriched') or (c.get('metadata') and c['metadata'].get('harvest_enriched')))
print("Harvest Enriched count:", harvest_count)

# Sample discarded contacts
discards = [c for c in data if c.get('crmStatus') == 'Descartado']
print(f"Sample discarded contact (total {len(discards)}):", discards[0] if discards else "None")
