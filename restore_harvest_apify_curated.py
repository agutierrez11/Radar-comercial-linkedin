import subprocess, json

# 1. Fetch exact enriched connections from commit e618921
cmd = ['git', 'show', 'e618921:enriched_connections.json']
res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
e61_data = json.loads(res)

print(f"Loaded {len(e61_data)} contacts from commit e618921")

# Check harvest and discards in e61_data
harvest_cnt = sum(1 for c in e61_data if c.get('harvest_enriched') or c.get('isHarvestEnriched') or (c.get('metadata') and c['metadata'].get('harvest_enriched')))
discards_cnt = sum(1 for c in e61_data if c.get('crmStatus') == 'Descartado' or c.get('discardedFromPurge'))
vigente_cnt = sum(1 for c in e61_data if 'Vigente' in str(c.get('jobStatus')) or 'Vigente' in str(c.get('job_status')) or c.get('is_current'))

print(f"Commit e618921 statistics:")
print(f" - Total Contacts: {len(e61_data)}")
print(f" - Harvest Enriched Profiles: {harvest_cnt}")
print(f" - Job Vigente (Apify/Live): {vigente_cnt}")
print(f" - Manual Discards: {discards_cnt}")

# 2. Write to enriched_connections.json
with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(e61_data, f, ensure_ascii=False, indent=2)
print("✅ Updated enriched_connections.json")

# 3. Write to master_data.json
master_dict = {
    "ownerName": "Antonio Gutiérrez",
    "contacts": e61_data
}
with open('master_data.json', 'w', encoding='utf-8') as f:
    json.dump(master_dict, f, ensure_ascii=False, indent=2)
print("✅ Updated master_data.json")

# 4. Write to master_data.js
js_code = f"window.__MASTER_DATA__ = {json.dumps(e61_data, ensure_ascii=False)};\n"
with open('master_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("✅ Updated master_data.js")
