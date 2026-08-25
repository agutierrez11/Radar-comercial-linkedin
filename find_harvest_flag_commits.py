import subprocess, json

commits = ['e618921', 'ce0e73a', '07f4b04', '9cc55d8', 'a86304e', 'HEAD']

for c in commits:
    try:
        res = subprocess.check_output(['git', 'show', f'{c}:enriched_connections.json'], encoding='utf-8', errors='replace')
        data = json.loads(res)
        
        harvest_flag = [item for item in data if item.get('harvest_enriched') or item.get('isHarvestEnriched') or (item.get('metadata') and item['metadata'].get('harvest_enriched'))]
        
        vigente_flag = [item for item in data if 'Vigente' in str(item.get('jobStatus')) or 'Vigente' in str(item.get('job_status')) or item.get('is_current')]
        
        print(f"Commit {c:10s} -> Total: {len(data):5d} | Harvest Enriched: {len(harvest_flag):4d} | Job Vigente: {len(vigente_flag):4d}")
        if len(harvest_flag) > 0:
            print("  └> Sample harvest contact name:", harvest_flag[0].get('name') or harvest_flag[0].get('first_name'))
    except Exception as e:
        print(f"Commit {c:10s} -> Error: {e}")
