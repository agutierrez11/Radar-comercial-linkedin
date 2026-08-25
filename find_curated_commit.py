import subprocess, json

commits = ['HEAD', '6344b49', '85f86fd', 'd7c5394', '6d8771c', '033c674', 'c089e92', 'db8d667', '9092992', '13fc3ef', '428af2f', '9cc55d8']

for c in commits:
    try:
        cmd = ['git', 'show', f'{c}:enriched_connections.json']
        res = subprocess.check_output(cmd, encoding='utf-8', errors='replace')
        data = json.loads(res)
        
        discards = sum(1 for item in data if item.get('crmStatus') == 'Descartado' or item.get('discardedFromPurge'))
        white = sum(1 for item in data if item.get('crmStatus') in ['Conservado', 'Protegido'] or item.get('whitelistedFromPurge'))
        harvest = sum(1 for item in data if item.get('harvest_enriched') or item.get('isHarvestEnriched') or (item.get('metadata') and item['metadata'].get('harvest_enriched')))
        
        print(f"Commit {c:10s} | Total: {len(data):5d} | Discards: {discards:4d} | Whitelisted: {white:4d} | Harvest: {harvest:4d}")
    except Exception as e:
        print(f"Commit {c:10s} | Error: {e}")
