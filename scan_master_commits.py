import subprocess, json

cmd = ['git', 'log', '--oneline', '-n', '30']
commits_out = subprocess.check_output(cmd, encoding='utf-8', errors='replace').splitlines()

for line in commits_out:
    c_hash = line.split()[0]
    msg = line[8:]
    try:
        res = subprocess.check_output(['git', 'show', f'{c_hash}:master_data.json'], encoding='utf-8', errors='replace')
        raw = json.loads(res)
        data = raw.get('contacts', []) if isinstance(raw, dict) else raw
        d_count = sum(1 for item in data if item.get('crmStatus') == 'Descartado' or item.get('discardedFromPurge'))
        w_count = sum(1 for item in data if item.get('crmStatus') == 'Conservado' or item.get('whitelistedFromPurge'))
        h_count = sum(1 for item in data if item.get('harvest_enriched') or item.get('isHarvestEnriched') or item.get('jobStatus') == 'Vigente')
        print(f"Commit {c_hash} ({msg[:35]}) -> Contacts: {len(data)} | Discards: {d_count} | Whitelisted: {w_count} | Harvest: {h_count}")
    except Exception as e:
        pass
