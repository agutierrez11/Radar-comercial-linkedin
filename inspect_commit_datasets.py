import json, subprocess

def inspect_json_str(raw_str, name):
    try:
        data = json.loads(raw_str)
        print(f"\n--- {name} ---")
        print(f"Total items: {len(data)}")
        if len(data) > 0:
            sample = data[0]
            print(f"Sample keys: {list(sample.keys())[:15]}")
            
            # Check fields
            discards = sum(1 for c in data if c.get('crmStatus') in ['Descartado', 'Archivado'] or c.get('discardedFromPurge'))
            white = sum(1 for c in data if c.get('crmStatus') in ['Conservado', 'Protegido'] or c.get('whitelistedFromPurge'))
            harvest = sum(1 for c in data if c.get('harvest_enriched') or c.get('isHarvestEnriched'))
            
            print(f"Discards count: {discards}")
            print(f"Whitelisted count: {white}")
            print(f"Harvest enriched count: {harvest}")
    except Exception as e:
        print(f"Error inspecting {name}: {e}")

# Inspect current enriched_connections.json
with open('enriched_connections.json', 'r', encoding='utf-8', errors='replace') as f:
    inspect_json_str(f.read(), 'Current enriched_connections.json')

# Inspect git commit db8d667:enriched_connections.json
try:
    cmd = ['git', 'show', 'db8d667:enriched_connections.json']
    res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
    inspect_json_str(res, 'Git commit db8d667:enriched_connections.json')
except Exception as e:
    print(f"Error reading git db8d667: {e}")

# Inspect git commit 428af2f:enriched_connections.json
try:
    cmd = ['git', 'show', '428af2f:enriched_connections.json']
    res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
    inspect_json_str(res, 'Git commit 428af2f:enriched_connections.json')
except Exception as e:
    print(f"Error reading git 428af2f: {e}")

# Inspect git commit 9092992:enriched_connections.json
try:
    cmd = ['git', 'show', '9092992:enriched_connections.json']
    res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
    inspect_json_str(res, 'Git commit 9092992:enriched_connections.json')
except Exception as e:
    print(f"Error reading git 9092992: {e}")
