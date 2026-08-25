import os, json, glob

json_files = glob.glob("*.json")
print("Found JSON files:", json_files)

for jf in json_files:
    if os.path.getsize(jf) > 100 * 1024 * 1024:
        print(f"Skipping large file {jf}")
        continue
    try:
        with open(jf, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if content.strip().startswith('[') or content.strip().startswith('{'):
                data = json.loads(content)
                if isinstance(data, list) and len(data) > 0:
                    discards = sum(1 for c in data if isinstance(c, dict) and (c.get('crmStatus') in ['Descartado', 'Archivado'] or c.get('discardedFromPurge')))
                    white = sum(1 for c in data if isinstance(c, dict) and (c.get('crmStatus') in ['Conservado', 'Protegido'] or c.get('whitelistedFromPurge')))
                    harvest = sum(1 for c in data if isinstance(c, dict) and (c.get('harvest_enriched') or c.get('isHarvestEnriched')))
                    print(f"File '{jf}': {len(data)} items | Discards: {discards} | Whitelisted: {white} | Harvest Enriched: {harvest}")
                elif isinstance(data, dict):
                    print(f"File '{jf}': dict with keys {list(data.keys())[:10]}")
    except Exception as e:
        print(f"Error reading {jf}: {e}")
