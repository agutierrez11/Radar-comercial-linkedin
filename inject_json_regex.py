import json
import re

with open('locations_normalized.json', 'r', encoding='utf-8') as f:
    loc_data = json.load(f)

json_str = json.dumps(loc_data, ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Buscamos el bloque viejo de window.normalizedLocations y lo reemplazamos
pattern = r'window\.normalizedLocations\s*=\s*\{.*?\};'
new_block = f'window.normalizedLocations = {json_str};'

new_html = re.sub(pattern, new_block, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("JSON actualizado en index.html con los resultados de Claude.")
