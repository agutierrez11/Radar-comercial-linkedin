import zipfile
import io
import csv
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

zip_path = r'C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip'
enriched_file = 'enriched_connections.json'

# 1. Cargar la base limpia
with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    contacts = json.load(f)

print(f"Base limpia cargada: {len(contacts)} contactos")

# Mapeo por URL limpia
url_to_contact_idx = {}
for idx, c in enumerate(contacts):
    u = (c.get('url') or '').strip().lower()
    u = re.sub(r'\?.*$', '', u).rstrip('/')
    if u:
        url_to_contact_idx[u] = idx

# Detectar el nombre del usuario (Antonio)
owner_name_counts = {}

convs = {} # conversation_id -> list of msgs

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
                
            # Contar emisor para saber quién es Antonio
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

# El sender_name más frecuente es Antonio
my_name = max(owner_name_counts.items(), key=lambda x: x[1])[0]
print(f"Usuario emisor principal detectado: '{my_name}' ({owner_name_counts[my_name]} mensajes)")

# Clasificador Heurístico / Semántico de Sentimiento y Respuesta Real
def analyze_sentiment_and_response(messages, my_name):
    # Ordenar mensajes cronológicamente
    messages.sort(key=lambda x: x['date'])
    
    # Separar mis mensajes y los del contacto
    my_msgs = [m for m in messages if m['sender_name'] == my_name]
    other_msgs = [m for m in messages if m['sender_name'] != my_name]
    
    if not my_msgs:
        return 'Iniciado por el Contacto', 'Sin Respuesta Necesaria', 'Neutro', False, False
        
    # Encontrar el primer mensaje enviado por mí
    first_my_msg = my_msgs[0]
    first_my_idx = messages.index(first_my_msg)
    
    # Respuestas posteriores del contacto
    subsequent_other = [m for m in messages[first_my_idx+1:] if m['sender_name'] != my_name]
    
    has_reply = len(subsequent_other) > 0
    
    if not has_reply:
        return 'Sin Respuesta (Ghosting)', 'Fantasma / Ignorado', 'Frio', False, False

    # Analizar el texto de las respuestas del contacto
    all_reply_text = " ".join([m['content'].lower() for m in subsequent_other])
    
    # Palabras clave de Sentimiento / Intent Comercial
    interest_keywords = [
        'interesa', 'interesado', 'interesada', 'me interesa', 'suena bien', 'excelente', 'perfecto',
        'agenda', 'agendemos', 'reunion', 'reunión', 'demostracion', 'demo', 'llamada', 'llámame',
        'cotizacion', 'cotización', 'propuesta', 'precios', 'cuanto cuesta', 'cuánto cuesta',
        'pasame tu', 'pásame tu', 'link', 'calendly', 'correo', 'mail', 'contacto', 'whatsapp'
    ]
    
    rejection_keywords = [
        'no gracias', 'no me interesa', 'por el momento no', 'ahora no', 'ya tenemos',
        'no estamos buscando', 'no tengo presupuesto', 'no es prioritario', 'baja de la lista',
        'gracias pero no', 'desconectar', 'spam'
    ]
    
    curiosity_keywords = [
        'de que se trata', 'de qué se trata', 'como funciona', 'cómo funciona', 'cuéntame mas',
        'cuéntame más', 'que hacen', 'qué hacen', 'detalles', 'info', 'información'
    ]

    is_high_interest = any(kw in all_reply_text for kw in interest_keywords)
    is_rejection = any(kw in all_reply_text for kw in rejection_keywords)
    is_curious = any(kw in all_reply_text for kw in curiosity_keywords)

    if is_high_interest:
        sentiment = '🟢 Interés Alto / Dispuesto a Demo'
        intent = 'Lead Cálido / Oportunidad Real'
        is_deal = True
    elif is_curious:
        sentiment = '🟡 Curiosidad / Evaluando'
        intent = 'Cualificación en Proceso'
        is_deal = False
    elif is_rejection:
        sentiment = '🔴 Objeción / Rechazo Abierto'
        intent = 'No Interesado / Cerrado'
        is_deal = False
    else:
        # Respuesta cortés o cordial sin intención comercial clara aún
        sentiment = '⚪ Respuesta Cortés / Networking Neutral'
        intent = 'Conversación Social'
        is_deal = False
        
    return 'Respondió', sentiment, intent, has_reply, is_deal

# Procesar todas las conversaciones y cruzarlas con los contactos
analyzed_stats = {
    'Sin Respuesta (Ghosting)': 0,
    '🟢 Interés Alto / Dispuesto a Demo': 0,
    '🟡 Curiosidad / Evaluando': 0,
    '🔴 Objeción / Rechazo Abierto': 0,
    '⚪ Respuesta Cortés / Networking Neutral': 0,
    'Iniciado por el Contacto': 0
}

contact_sentiments = {}

for cid, msgs in convs.items():
    cat, sentiment, intent, has_reply, is_deal = analyze_sentiment_and_response(msgs, my_name)
    analyzed_stats[sentiment] = analyzed_stats.get(sentiment, 0) + 1
    
    # Identificar la URL o nombre del contacto con quien chateé
    other_urls = set()
    for m in msgs:
        if m['sender_name'] != my_name and m['sender_url']:
            other_urls.add(m['sender_url'])
        # Buscar destinatarios
        for u in re.findall(r'https?://[^\s,\"]+', m['recipients_str']):
            u_clean = re.sub(r'\?.*$', '', u.strip().lower()).rstrip('/')
            if u_clean and u_clean in url_to_contact_idx:
                other_urls.add(u_clean)
                
    for u in other_urls:
        if u in url_to_contact_idx:
            c_idx = url_to_contact_idx[u]
            contact_sentiments[c_idx] = {
                'sentiment': sentiment,
                'intent': intent,
                'has_reply': has_reply,
                'is_deal': is_deal,
                'turns': len(msgs),
                'last_reply_snippet': msgs[-1]['content'][:150]
            }

print("\n=== RESUMEN DE ANÁLISIS DE SENTIMIENTO DE DMs DE LINKEDIN ===")
for k, v in analyzed_stats.items():
    print(f"{k}: {v} conversaciones")

# Inyectar estos sentimientos reales en enriched_connections.json
for idx, c in enumerate(contacts):
    if idx in contact_sentiments:
        c['sentiment'] = contact_sentiments[idx]['sentiment']
        c['intent'] = contact_sentiments[idx]['intent']
        c['has_reply'] = contact_sentiments[idx]['has_reply']
        c['is_deal'] = contact_sentiments[idx]['is_deal']
        c['turns'] = contact_sentiments[idx]['turns']
        c['last_reply_snippet'] = contact_sentiments[idx]['last_reply_snippet']
    else:
        c['sentiment'] = '⚪ Sin Conversación (0 Mensajes)'
        c['intent'] = 'Sin Contacto'
        c['has_reply'] = False
        c['is_deal'] = False
        c['turns'] = 0

with open(enriched_file, 'w', encoding='utf-8') as f:
    json.dump(contacts, f, ensure_ascii=False, indent=2)

print("\n¡Inyección de Sentimiento de Mensajes completada exitosamente en enriched_connections.json!")
