import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Procesando saneamiento de {len(data)} contactos...')

cleaned_count = 0
unknown_fixed = 0

for c in data:
    comp = str(c.get('company', '') or '')
    pos = str(c.get('position', '') or '')
    
    # 1. Limpieza de strings sucios como '98,173 followers' o 'followers'
    if re.search(r'\b\d+[\d,.]*\s*(followers?|seguidores?)\b', comp, re.I) or 'follower' in comp.lower():
        c['company'] = ''
        c['company_zip'] = ''
        cleaned_count += 1
    if re.search(r'\b\d+[\d,.]*\s*(followers?|seguidores?)\b', pos, re.I) or 'follower' in pos.lower():
        c['position'] = ''
        c['position_current'] = ''
        cleaned_count += 1

    # 2. Inferencia estricta de país por empresa / universidad / cargo si está en Desconocido
    country = c.get('country', 'Desconocido')
    if not country or country == 'Desconocido':
        text = f"{c.get('email','')} {c.get('company','')} {c.get('position','')} {c.get('full_name','')}".lower()
        if any(k in text for k in ['mexico', 'cdmx', 'monterrey', 'guadalajara', 'cancun', 'queretaro', 'puebla', 'tijuana', 'merida', 'zapopan', 'toluca', 'unam', 'itesm', 'ipn', 'anahuac', 'ibero', 'itam', 'banamex', 'banorte', 'clip', 'fiserv', 'konfio', 'kueski', 'stori', 'kavak', 'elektra', 'liverpool', 'bbva mexico']):
            c['country'] = 'México'
            c['city'] = 'CDMX'
            c['lat'] = 23.6345
            c['lng'] = -102.5528
            unknown_fixed += 1
        elif any(k in text for k in ['chile', 'santiago', 'valparaiso', 'fintoc', 'falabella', 'banco de chile', 'uchile', 'puc']):
            c['country'] = 'Chile'
            c['city'] = 'Santiago'
            c['lat'] = -35.6751
            c['lng'] = -71.5430
            unknown_fixed += 1
        elif any(k in text for k in ['colombia', 'bogota', 'medellin', 'cali', 'rappi', 'bold', 'bancolombia', 'uniandes', 'javeriana']):
            c['country'] = 'Colombia'
            c['city'] = 'Bogotá'
            c['lat'] = 4.5709
            c['lng'] = -74.2973
            unknown_fixed += 1
        elif any(k in text for k in ['peru', 'perú', 'lima', 'yape', 'interbank', 'bcp', 'pucp']):
            c['country'] = 'Perú'
            c['city'] = 'Lima'
            c['lat'] = -9.1900
            c['lng'] = -75.0152
            unknown_fixed += 1
        elif any(k in text for k in ['brasil', 'brazil', 'sao paulo', 'rio de janeiro', 'nubank', 'stone', 'pagseguro', 'pix']):
            c['country'] = 'Brasil'
            c['city'] = 'São Paulo'
            c['lat'] = -14.2350
            c['lng'] = -51.9253
            unknown_fixed += 1
        elif any(k in text for k in ['argentina', 'buenos aires', 'utn', 'uba', 'mercadolibre', 'ualá', 'prisma']):
            c['country'] = 'Argentina'
            c['city'] = 'Buenos Aires'
            c['lat'] = -38.4161
            c['lng'] = -63.6167
            unknown_fixed += 1
        elif any(k in text for k in ['espana', 'spain', 'madrid', 'barcelona', 'bbva', 'santander']):
            c['country'] = 'España'
            c['city'] = 'Madrid'
            c['lat'] = 40.4637
            c['lng'] = -3.7492
            unknown_fixed += 1
        elif any(k in text for k in ['usa', 'united states', 'miami', 'new york', 'california', 'texas', 'san francisco', 'florida', 'stripe', 'dlocal', 'nuvei']):
            c['country'] = 'Estados Unidos'
            c['city'] = 'Miami'
            c['lat'] = 37.0902
            c['lng'] = -95.7129
            unknown_fixed += 1

with open('enriched_connections.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✅ Limpieza finalizada: {cleaned_count} registros de seguidores corregidos y {unknown_fixed} países inferidos.')
