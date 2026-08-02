import json
import zipfile
import io
import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

zip_path = r'C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip'
enriched_file = 'enriched_connections.json'

with open(enriched_file, 'r', encoding='utf-8') as f:
    contacts = json.load(f)

url_to_contact_idx = {}
for idx, c in enumerate(contacts):
    u = (c.get('url') or '').strip().lower()
    u = re.sub(r'\?.*$', '', u).rstrip('/')
    if u:
        url_to_contact_idx[u] = idx

owner_name_counts = {}
convs = {}

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('messages.csv') as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        header = next(reader)
        
        cid_idx = header.index('CONVERSATION ID')
        from_idx = header.index('FROM')
        sender_url_idx = header.index('SENDER PROFILE URL')
        recipients_url_idx = header.index('RECIPIENT PROFILE URLS')
        date_idx = header.index('DATE')
        content_idx = header.index('CONTENT')
        
        for row in reader:
            if len(row) <= max(cid_idx, from_idx, sender_url_idx, recipients_url_idx, date_idx, content_idx):
                continue
                
            cid = row[cid_idx].strip()
            sender_name = row[from_idx].strip()
            sender_url = re.sub(r'\?.*$', '', row[sender_url_idx].strip().lower()).rstrip('/')
            recipients_str = row[recipients_url_idx]
            content = row[content_idx].strip()
            date_str = row[date_idx].strip()
            
            if not cid or not content:
                continue
                
            owner_name_counts[sender_name] = owner_name_counts.get(sender_name, 0) + 1
            
            if cid not in convs:
                convs[cid] = []
                
            convs[cid].append({
                'sender_name': sender_name,
                'sender_url': sender_url,
                'recipients_str': recipients_str,
                'date': date_str,
                'content': content
            })

my_name = max(owner_name_counts.items(), key=lambda x: x[1])[0]

# Palabras clave de VENTA INBOUND (Ellos intentan venderle a Antonio)
inbound_sales_pitch_keywords = [
    'te ofrezco', 'ofrecemos', 'nuestra plataforma', 'nuestros servicios', 'agendar una llamada contigo',
    'demo de nuestro', 'nuestra agencia', 'te gustaria conocer', 'te gustaría conocer', 'somos expertos en',
    'incrementar tus ventas', 'optimizamos tu', 'software para', 'te presento a', 'reunion de 15 min',
    'reunión de 15 min', 'desarrollo de software', 'servicios de reclutamiento', 'headhunting'
]

# Palabras clave de SALUDO AMISTOSO / AMIGOS / NETWORKING
friendly_keywords = [
    'feliz cumpleaños', 'feliz cumple', 'felicitaciones por el nuevo', 'felicidades', 'abrazo', 'saludos a la familia',
    'que gusto saber de ti', 'qué gusto saber de ti', 'como has estado', 'cómo has estado', 'amigo', 'amiga',
    'nos vemos pronto', 'tomar un cafe', 'tomar un café', 'exito', 'éxito', 'saludos'
]

def analyze_conversation_direction_and_intent(messages, my_name):
    messages.sort(key=lambda x: x['date'])
    first_msg = messages[0]
    
    first_is_me = (first_msg['sender_name'] == my_name)
    
    other_msgs = [m for m in messages if m['sender_name'] != my_name]
    my_msgs = [m for m in messages if m['sender_name'] == my_name]
    
    full_text_other = " ".join([m['content'].lower() for m in other_msgs])
    full_text_all = " ".join([m['content'].lower() for m in messages])
    
    # 1. ¿Detecta si el contacto le está vendiendo a Antonio? (INBOUND PITCH)
    is_they_selling = (not first_is_me) and any(kw in full_text_other for kw in inbound_sales_pitch_keywords)
    
    # 2. ¿Es un saludo amigable / amistad sin tono de ventas?
    is_friendly = any(kw in full_text_all for kw in friendly_keywords) and not any(kw in full_text_all for kw in ['demo', 'cotizacion', 'propuesta', 'comprar', 'cliente'])
    
    # Direccionalidad
    if is_they_selling:
        direction = '📥 Ellos intentaron venderte a ti (Inbound Pitch)'
    elif first_is_me:
        direction = '📤 Outbound (Tú iniciaste)'
    else:
        direction = '📥 Inbound Contact (Ellos iniciaron)'

    # Sentimiento / Tipo de relación
    if is_they_selling:
        sentiment_label = '💼 Prospectador Externo (Te busca ofrecer servicio)'
    elif is_friendly:
        sentiment_label = '🤝 Saludo Amistoso / Conexión Social'
    elif len(other_msgs) == 0 and first_is_me:
        sentiment_label = '👻 Fantasma (0 Respuestas)'
    elif len(other_msgs) > 0 and first_is_me:
        if any(kw in full_text_other for kw in ['interesa', 'demo', 'reunion', 'agendemos', 'link', 'whatsapp']):
            sentiment_label = '🟢 Oportunidad Comercial Real (Le vendiste a ellos)'
        elif any(kw in full_text_other for kw in ['no gracias', 'no me interesa', 'ahora no']):
            sentiment_label = '🔴 Objeción / Desinterés'
        else:
            sentiment_label = '⚪ Respuesta Cortés / Charla General'
    else:
        sentiment_label = '💬 Conversación General'
        
    return direction, sentiment_label, is_they_selling, is_friendly

stats = {
    'Inbound Pitches (Ellos te venden)': 0,
    'Outbound Tuio (Tú vendes / contactas)': 0,
    'Saludos Amistosos / Social': 0
}

contact_analysis = {}

for cid, msgs in convs.items():
    direction, sentiment_label, is_they_selling, is_friendly = analyze_conversation_direction_and_intent(msgs, my_name)
    
    if is_they_selling:
        stats['Inbound Pitches (Ellos te venden)'] += 1
    elif is_friendly:
        stats['Saludos Amistosos / Social'] += 1
    else:
        stats['Outbound Tuio (Tú vendes / contactas)'] += 1
        
    other_urls = set()
    for m in msgs:
        if m['sender_name'] != my_name and m['sender_url']:
            other_urls.add(m['sender_url'])
        for u in re.findall(r'https?://[^\s,\"]+', m['recipients_str']):
            u_clean = re.sub(r'\?.*$', '', u.strip().lower()).rstrip('/')
            if u_clean and u_clean in url_to_contact_idx:
                other_urls.add(u_clean)
                
    for u in other_urls:
        if u in url_to_contact_idx:
            c_idx = url_to_contact_idx[u]
            contact_analysis[c_idx] = {
                'direction': direction,
                'sentiment_detail': sentiment_label,
                'is_they_selling': is_they_selling,
                'is_friendly': is_friendly
            }

print("=== RESULTADOS DEL ANÁLISIS DE DIRECCIONALIDAD DE VENTAS Y SALUDOS AMISTOSOS ===")
for k, v in stats.items():
    print(f"{k}: {v}")

# Inyectar en enriched_connections.json
for idx, c in enumerate(contacts):
    if idx in contact_analysis:
        c['direction'] = contact_analysis[idx]['direction']
        c['sentiment_detail'] = contact_analysis[idx]['sentiment_detail']
        c['is_they_selling'] = contact_analysis[idx]['is_they_selling']
        c['is_friendly'] = contact_analysis[idx]['is_friendly']
    else:
        c['direction'] = 'Sin Conversación'
        c['sentiment_detail'] = '⚪ 0 Mensajes en LinkedIn'
        c['is_they_selling'] = False
        c['is_friendly'] = False

with open(enriched_file, 'w', encoding='utf-8') as f:
    json.dump(contacts, f, ensure_ascii=False, indent=2)

print("\n¡Inyección de Direccionalidad y Saludos Amistosos completada con éxito!")
