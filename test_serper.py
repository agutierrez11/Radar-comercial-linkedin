import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://google.serper.dev/search'
headers = {
    'X-API-KEY': 'c81b4a514d4a055cdb94c624db56aef2fa879772',
    'Content-Type': 'application/json'
}

queries = [
    'site:linkedin.com/in/ezequielguerrero',
    'site:linkedin.com/in/ "Kevin JI"',
    'site:linkedin.com/in/angelicacorreia',
]

for q in queries:
    print(f"\nQuery: {q}")
    data = json.dumps({'q': q}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if 'organic' in res and len(res['organic']) > 0:
                for item in res['organic'][:2]:
                    print(' Title:', item.get('title', ''))
                    print(' Snippet:', item.get('snippet', ''))
            else:
                print(' No organic results')
    except Exception as e:
        print('Error:', e)
