import os, json, urllib.request

env_path = '.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('APIFY_API_TOKEN='):
            token = line.strip().split('=', 1)[1]

dataset_id = '1IMAWhU4IM4v1h2sc'
url = f'https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&limit=1'
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data and 'author' in data[0]:
            print("Author keys:", list(data[0]['author'].keys()))
            print("Author object:", json.dumps(data[0]['author'], indent=2))
except Exception as e:
    print('Error:', e)
