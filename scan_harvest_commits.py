import subprocess, json

cmd = ['git', 'log', '--oneline', '-n', '30']
commits_out = subprocess.check_output(cmd, encoding='utf-8', errors='replace').splitlines()

print(f"Scanning {len(commits_out)} commits...")
for line in commits_out:
    c_hash = line.split()[0]
    msg = line[8:]
    try:
        res = subprocess.check_output(['git', 'show', f'{c_hash}:enriched_connections.json'], encoding='utf-8', errors='replace')
        data = json.loads(res)
        h_count = sum(1 for item in data if item.get('harvest_enriched') or item.get('isHarvestEnriched') or item.get('jobStatus') == 'Vigente' or (item.get('metadata') and item['metadata'].get('harvest_enriched')))
        d_count = sum(1 for item in data if item.get('crmStatus') == 'Descartado' or item.get('discardedFromPurge'))
        if h_count > 0 or d_count == 86:
            print(f"Commit {c_hash} ({msg[:40]}) -> Total: {len(data)} | Harvest/Vigente: {h_count} | Discards: {d_count}")
    except Exception:
        pass
