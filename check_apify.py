import os, json, urllib.request

env_path = '.env'
token = None
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('APIFY_API_TOKEN='):
                token = line.strip().split('=', 1)[1]

if not token:
    print('No token')
else:
    url = f'https://api.apify.com/v2/actor-runs?token={token}&limit=5&desc=true'
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            runs = data['data']['items']
            for r in runs:
                print(f"Run ID: {r['id']}, Actor: {r.get('actId')}, Status: {r['status']}, Dataset: {r.get('defaultDatasetId')}")
    except Exception as e:
        print('Error:', e)
