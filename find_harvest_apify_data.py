import subprocess, json, os, glob

print("=== SEARCHING HARVEST & APIFY ENRICHED CONTACTS ACROSS REPOSITORY ===")

# 1. Search in local JSON files
json_files = glob.glob("*.json")
for jf in json_files:
    if os.path.getsize(jf) > 100 * 1024 * 1024: continue
    try:
        with open(jf, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if content.strip().startswith('[') or content.strip().startswith('{'):
                raw = json.loads(content)
                data = raw.get('contacts', raw) if isinstance(raw, dict) else raw
                if isinstance(data, list):
                    harvest_count = 0
                    apify_count = 0
                    active_count = 0
                    for c in data:
                        if isinstance(c, dict):
                            # Check harvest
                            if c.get('harvest_enriched') or c.get('isHarvestEnriched') or (c.get('metadata') and c['metadata'].get('harvest_enriched')):
                                harvest_count += 1
                            # Check apify or current_position/jobStatus
                            if c.get('apify_enriched') or c.get('jobStatus') == 'Vigente' or c.get('is_current') or (c.get('metadata') and c['metadata'].get('apify_enriched')):
                                apify_count += 1
                            # Check active (non-discarded)
                            if c.get('crmStatus') != 'Descartado' and not c.get('discardedFromPurge'):
                                active_count += 1
                    if harvest_count > 0 or apify_count > 0:
                        print(f"File '{jf}' -> Total: {len(data)} | Active (Depurados): {active_count} | Harvest: {harvest_count} | Apify/Vigente: {apify_count}")
    except Exception as e:
        pass

# 2. Search git commit history for commits mentioning Harvest or Apify
cmd = ['git', 'log', '--grep=Harvest', '--grep=Apify', '--oneline']
try:
    commits = subprocess.check_output(cmd, encoding='utf-8', errors='replace').splitlines()
    print(f"\nFound {len(commits)} commits mentioning Harvest/Apify:")
    for c in commits[:10]:
        c_hash = c.split()[0]
        msg = c[8:]
        print(f" - {c_hash}: {msg}")
        # Check enriched_connections.json in that commit
        try:
            res = subprocess.check_output(['git', 'show', f'{c_hash}:enriched_connections.json'], encoding='utf-8', errors='replace')
            data = json.loads(res)
            h_cnt = sum(1 for item in data if item.get('harvest_enriched') or item.get('isHarvestEnriched') or (item.get('metadata') and item['metadata'].get('harvest_enriched')))
            a_cnt = sum(1 for item in data if item.get('apify_enriched') or item.get('jobStatus') == 'Vigente' or item.get('is_current'))
            act_cnt = sum(1 for item in data if item.get('crmStatus') != 'Descartado' and not item.get('discardedFromPurge'))
            print(f"   └> enriched_connections.json -> Total: {len(data)} | Active: {act_cnt} | Harvest: {h_cnt} | Apify/Vigente: {a_cnt}")
        except Exception as e:
            pass
except Exception as e:
    print("Git grep error:", e)
