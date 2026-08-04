import os, urllib.request, json
env_path = '.env'
token = None
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('APIFY_API_TOKEN='):
                token = line.strip().split('=', 1)[1]
url = f'https://api.apify.com/v2/acts?search=linkedin&limit=20&token={token}'
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        for item in data['data']['items']:
            print(f"{item['id']} / {item['name']} ({item['username']}) / {item.get('title')}")
except Exception as e:
    print('Error:', e)

