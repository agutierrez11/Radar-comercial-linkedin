import urllib.request
import json
import re
import html
import sys

def get_deep(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
    })
    html_content = urllib.request.urlopen(req).read().decode('utf-8')
    
    title_m = re.search(r'<title>(.*?)</title>', html_content)
    title = title_m.group(1) if title_m else 'No title'
    
    # Try finding ytInitialPlayerResponse
    m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});(?:var|script)', html_content, re.DOTALL)
    if not m:
        m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html_content)
        
    if m:
        try:
            data = json.loads(m.group(1))
            captions = data.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks', [])
            print(f"[{video_id}] Found {len(captions)} caption tracks in ytInitialPlayerResponse")
            for c in captions:
                print("Track:", c.get('languageCode'), c.get('name', {}).get('simpleText'))
                cap_req = urllib.request.Request(c.get('baseUrl'), headers={'User-Agent': 'Mozilla/5.0'})
                xml_text = urllib.request.urlopen(cap_req).read().decode('utf-8')
                lines = re.findall(r'<text[^>]*>(.*?)</text>', xml_text)
                clean_lines = [html.unescape(l) for l in lines]
                full_text = ' '.join(clean_lines)
                return title, full_text
        except Exception as e:
            print("Error parsing json:", e)

    # Alternative: search web or yt-dlp
    return title, ""

t1, text1 = get_deep('f750ORi1-ws')
print(f"V1 Title: {t1}, Text len: {len(text1)}")
if text1:
    with open('transcript_v1.txt', 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {t1}\n\nTRANSCRIPT:\n{text1}")

t2, text2 = get_deep('hS8hSusH5ck')
print(f"V2 Title: {t2}, Text len: {len(text2)}")
if text2:
    with open('transcript_v2.txt', 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {t2}\n\nTRANSCRIPT:\n{text2}")
