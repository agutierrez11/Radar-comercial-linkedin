import json
import zipfile
import io
import csv
import re

enriched_file = 'enriched_connections.json'
zip_path = r'C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip'

with open(enriched_file, 'r', encoding='utf-8') as f:
    contacts = json.load(f)

print(f"Contactos cargados desde base limpia: {len(contacts)}")

url_map = {}
for idx, c in enumerate(contacts):
    u = (c.get('url') or '').strip().lower()
    u = re.sub(r'\?.*$', '', u).rstrip('/')
    if u:
        url_map[u] = idx

msg_count = 0
matched_contacts = set()

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('messages.csv') as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        header = next(reader)
        
        sender_idx = header.index('SENDER PROFILE URL')
        recipients_idx = header.index('RECIPIENT PROFILE URLS')
        date_idx = header.index('DATE')
        content_idx = header.index('CONTENT')

        for row in reader:
            if len(row) <= max(sender_idx, recipients_idx, date_idx, content_idx):
                continue
            msg_count += 1
            sender_url = re.sub(r'\?.*$', '', row[sender_idx].strip().lower()).rstrip('/')
            recipients_str = row[recipients_idx]
            content = row[content_idx]
            date_str = row[date_idx]
            
            r_urls = [re.sub(r'\?.*$', '', u.strip().lower()).rstrip('/') for u in re.findall(r'https?://[^\s,\"]+', recipients_str)]
            
            matched_idx = None
            if sender_url in url_map:
                matched_idx = url_map[sender_url]
            else:
                for ru in r_urls:
                    if ru in url_map:
                        matched_idx = url_map[ru]
                        break
            
            if matched_idx is not None:
                matched_contacts.add(matched_idx)
                c_obj = contacts[matched_idx]
                c_obj['msg_count'] = c_obj.get('msg_count', 0) + 1
                c_obj['last_msg_date'] = date_str
                c_obj['last_msg_snippet'] = content[:150]

print(f"Total mensajes procesados del ZIP: {msg_count}")
print(f"Contactos limpios que tienen mensajes cruzados: {len(matched_contacts)}")

# Guardar de vuelta manteniendo los 3,039 contactos y sus datos de Apify intactos
with open(enriched_file, 'w', encoding='utf-8') as f:
    json.dump(contacts, f, ensure_ascii=False, indent=2)

print("¡Merge perfecto completado! Se inyectaron los mensajes sin tocar ningún dato de Apify.")
