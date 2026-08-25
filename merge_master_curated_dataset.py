import subprocess, json

# 1. Load commit e618921 (HarvestAPI 404 + Vigente 1134)
cmd1 = ['git', 'show', 'e618921:enriched_connections.json']
e61_data = json.loads(subprocess.check_output(cmd1, encoding='utf-8', errors='replace'))

# 2. Load commit 13fc3ef (86 manual discards)
cmd2 = ['git', 'show', '13fc3ef:enriched_connections.json']
d13_data = json.loads(subprocess.check_output(cmd2, encoding='utf-8', errors='replace'))

# Create mapping of discarded contact IDs/urls
discarded_ids = set()
for c in d13_data:
    if c.get('crmStatus') == 'Descartado' or c.get('discardedFromPurge'):
        cid = str(c.get('id') or c.get('url') or c.get('name'))
        discarded_ids.add(cid)

print(f"[Merge] Found {len(discarded_ids)} manual discards from commit 13fc3ef.")

# Apply discards to e61_data
merged_contacts = []
harvest_cnt = 0
vigente_cnt = 0
discard_cnt = 0

for c in e61_data:
    cid = str(c.get('id') or c.get('url') or c.get('name'))
    if cid in discarded_ids:
        c['crmStatus'] = 'Descartado'
        c['discardedFromPurge'] = True
        discard_cnt += 1
    
    if c.get('harvest_enriched') or c.get('isHarvestEnriched'):
        harvest_cnt += 1
    if 'Vigente' in str(c.get('jobStatus')) or 'Vigente' in str(c.get('job_status')) or c.get('is_current'):
        vigente_cnt += 1
    
    merged_contacts.append(c)

print(f"[Merge Complete]")
print(f" - Total Contacts: {len(merged_contacts)}")
print(f" - Harvest Enriched Profiles: {harvest_cnt}")
print(f" - Job Vigente Profiles: {vigente_cnt}")
print(f" - Manual Discards Restored: {discard_cnt}")

# Save to files
with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(merged_contacts, f, ensure_ascii=False, indent=2)

master_dict = {
    "ownerName": "Antonio Gutiérrez",
    "contacts": merged_contacts
}
with open('master_data.json', 'w', encoding='utf-8') as f:
    json.dump(master_dict, f, ensure_ascii=False, indent=2)

js_code = f"window.__MASTER_DATA__ = {json.dumps(merged_contacts, ensure_ascii=False)};\n"
with open('master_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("[INFO] Files updated cleanly.")
