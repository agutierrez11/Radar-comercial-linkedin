import urllib.request
import json
import traceback

try:
    req = urllib.request.Request('https://api.github.com/users/HarvestAPI/repos', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())
        for r in repos:
            print(f"Repo: {r['name']} - {r['description']}")
except Exception as e:
    print('Error:', e)
    traceback.print_exc()
