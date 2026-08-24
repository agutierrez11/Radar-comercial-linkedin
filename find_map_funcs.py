with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', content)
map_funcs = [fn for fn in funcs if 'map' in fn.lower() or 'gis' in fn.lower() or 'net' in fn.lower() or 'filter' in fn.lower()]
print("Map/Network/Filter related functions:", map_funcs)
