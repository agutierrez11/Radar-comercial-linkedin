import urllib.request
import json
import re
import html
import xml.etree.ElementTree as ET

def get_transcript(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        page_html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        return f"Error loading video page: {e}", ""

    title_m = re.search(r'<title>(.*?)</title>', page_html)
    title = title_m.group(1).replace(' - YouTube', '') if title_m else 'No title'
    
    m = re.search(r'\"captionTracks\":(\[.*?\])', page_html)
    if not m:
        return title, "No captions found in player"
    
    try:
        tracks = json.loads(m.group(1))
    except Exception as e:
        return title, f"Error parsing caption tracks: {e}"

    selected_url = None
    for tr in tracks:
        lang = tr.get('languageCode', '')
        if lang in ['es', 'en', 'es-419']:
            selected_url = tr.get('baseUrl')
            break
    if not selected_url and tracks:
        selected_url = tracks[0].get('baseUrl')
        
    if not selected_url:
        return title, "No caption track URL"
        
    try:
        cap_xml = urllib.request.urlopen(selected_url).read().decode('utf-8')
        root = ET.fromstring(cap_xml)
        lines = []
        for child in root.findall('text'):
            txt = child.text
            if txt:
                lines.append(html.unescape(txt.strip()))
        return title, ' '.join(lines)
    except Exception as e:
        return title, f"Error fetching caption xml: {e}"

t1, c1 = get_transcript('f750ORi1-ws')
print(f"=== VIDEO 1 (f750ORi1-ws) ===")
print(f"Title: {t1}")
print(f"Transcript Length: {len(c1)} characters")

t2, c2 = get_transcript('hS8hSusH5ck')
print(f"\n=== VIDEO 2 (hS8hSusH5ck) ===")
print(f"Title: {t2}")
print(f"Transcript Length: {len(c2)} characters")

with open('transcript_v1.txt', 'w', encoding='utf-8') as f:
    f.write(f"TITLE: {t1}\n\nTRANSCRIPT:\n{c1}")

with open('transcript_v2.txt', 'w', encoding='utf-8') as f:
    f.write(f"TITLE: {t2}\n\nTRANSCRIPT:\n{c2}")
