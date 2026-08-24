import urllib.request
import json
import re

url = "https://www.youtube.com/watch?v=f750ORi1-ws"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
html_content = urllib.request.urlopen(req).read().decode('utf-8')
m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html_content)
data = json.loads(m.group(1))
captions = data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])

print("Captions tracks:", captions)
if captions:
    burl = captions[0]['baseUrl']
    print("Base URL:", burl)
    res = urllib.request.urlopen(burl).read().decode('utf-8')
    print("RAW RES (first 500 chars):", repr(res[:500]))
    with open('raw_cap.xml', 'w', encoding='utf-8') as f:
        f.write(res)
