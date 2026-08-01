import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("enriched_connections.json", "r", encoding="utf-8") as f:
    enriched_data = json.load(f)

json_str = json.dumps(enriched_data, ensure_ascii=False)

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Reemplazar la asignación de window.ENRICHED_CONNECTIONS_DATA o insertarla
script_block = f'<script>\nwindow.ENRICHED_CONNECTIONS_DATA = {json_str};\n</script>\n</head>'

if "window.ENRICHED_CONNECTIONS_DATA =" in html_content:
    import re
    html_content = re.sub(r'<script>\s*window\.ENRICHED_CONNECTIONS_DATA =.*?</script>', f'<script>\nwindow.ENRICHED_CONNECTIONS_DATA = {json_str};\n</script>', html_content, flags=re.DOTALL)
else:
    html_content = html_content.replace('</head>', script_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Datos embebidos en index.html sin CORS ni bloqueos de file://")
