import urllib.request
import json
import re
import html

def get_raw_captions(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    html_content = urllib.request.urlopen(req).read().decode('utf-8')
    
    title_m = re.search(r'<title>(.*?)</title>', html_content)
    title = title_m.group(1).replace(' - YouTube', '') if title_m else 'No title'
    
    m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html_content)
    if not m:
        return title, ""
        
    data = json.loads(m.group(1))
    captions = data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
    if not captions:
        return title, ""
        
    base_url = captions[0].get('baseUrl')
    # Try fetching as json or xml
    cap_url = base_url + "&fmt=json3"
    cap_req = urllib.request.Request(cap_url, headers={'User-Agent': 'Mozilla/5.0'})
    res_text = urllib.request.urlopen(cap_req).read().decode('utf-8')
    
    full_text = ""
    try:
        cap_json = json.loads(res_text)
        events = cap_json.get('events', [])
        lines = []
        for ev in events:
            segs = ev.get('segs', [])
            for s in segs:
                utf8 = s.get('utf8', '')
                if utf8 and utf8 != '\n':
                    lines.append(utf8)
        full_text = ''.join(lines)
    except Exception as e:
        print("JSON parse error:", e)
        # Fallback to regex on raw text
        clean = re.sub(r'<[^>]+>', ' ', res_text)
        full_text = html.unescape(clean)
        
    return title, full_text

t1, c1 = get_raw_captions('f750ORi1-ws')
print(f"Video 1 Title: {t1}")
print(f"Transcript 1 Length: {len(c1)}")

t2, c2 = get_raw_captions('hS8hSusH5ck')
print(f"Video 2 Title: {t2}")
print(f"Transcript 2 Length: {len(c2)}")

with open('transcript_v1.txt', 'w', encoding='utf-8') as f:
    f.write(f"TITLE: {t1}\n\nTRANSCRIPT:\n{c1}")

with open('transcript_v2.txt', 'w', encoding='utf-8') as f:
    f.write(f"TITLE: {t2}\n\nTRANSCRIPT:\n{c2}")
