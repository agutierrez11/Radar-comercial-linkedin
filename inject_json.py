import json
import sys

with open('locations_normalized.json', 'r', encoding='utf-8') as f:
    loc_data = json.load(f)

json_str = json.dumps(loc_data, ensure_ascii=False)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update inferCountry
old_infer = """function inferCountry(email, company, position) {
  const e = (email||'').toLowerCase();
  const b = norm(`${company} ${position}`);
  if (e.endsWith('.mx')) return 'México';
  if (e.endsWith('.cl')) return 'Chile';
  if (e.endsWith('.co')) return 'Colombia';
  if (e.endsWith('.pe')) return 'Perú';
  if (e.endsWith('.br')) return 'Brasil';
  if (e.endsWith('.ar')) return 'Argentina';
  if (e.endsWith('.es')) return 'España';
  if (/\\b(mexico|cdmx|monterrey|guadalajara|cancun|queretaro)\\b/.test(b)) return 'México';
  if (/\\b(chile|santiago)\\b/.test(b)) return 'Chile';
  if (/\\b(colombia|bogota|medellin)\\b/.test(b)) return 'Colombia';
  if (/\\b(peru|lima)\\b/.test(b)) return 'Perú';
  if (/\\b(brasil|brazil|sao paulo|rio)\\b/.test(b)) return 'Brasil';
  if (/\\b(argentina|buenos aires|cordoba)\\b/.test(b)) return 'Argentina';
  if (/\\b(espana|spain|madrid|barcelona)\\b/.test(b)) return 'España';
  if (/\\b(usa|united states|new york|san francisco|chicago|houston)\\b/.test(b)) return 'USA';
  return 'Desconocido';
}"""

new_infer = """function inferCountry(email, company, position) {
  const key = `${(company||'').trim()} | ${(position||'').trim()}`;
  if (window.normalizedLocations && window.normalizedLocations[key]) {
      const c = window.normalizedLocations[key].country;
      if (c && c !== 'Desconocido') return c;
  }
  
  const e = (email||'').toLowerCase();
  const b = norm(`${company} ${position}`);
  if (e.endsWith('.mx')) return 'México';
  if (e.endsWith('.cl')) return 'Chile';
  if (e.endsWith('.co')) return 'Colombia';
  if (e.endsWith('.pe')) return 'Perú';
  if (e.endsWith('.br')) return 'Brasil';
  if (e.endsWith('.ar')) return 'Argentina';
  if (e.endsWith('.es')) return 'España';
  if (/\\b(mexico|cdmx|monterrey|guadalajara|cancun|queretaro)\\b/.test(b)) return 'México';
  if (/\\b(chile|santiago)\\b/.test(b)) return 'Chile';
  if (/\\b(colombia|bogota|medellin)\\b/.test(b)) return 'Colombia';
  if (/\\b(peru|lima)\\b/.test(b)) return 'Perú';
  if (/\\b(brasil|brazil|sao paulo|rio)\\b/.test(b)) return 'Brasil';
  if (/\\b(argentina|buenos aires|cordoba)\\b/.test(b)) return 'Argentina';
  if (/\\b(espana|spain|madrid|barcelona)\\b/.test(b)) return 'España';
  if (/\\b(usa|united states|new york|san francisco|chicago|houston)\\b/.test(b)) return 'USA';
  return 'Desconocido';
}"""

if old_infer in html:
    html = html.replace(old_infer, new_infer)
else:
    print("No se encontró la función inferCountry exacta. Revisa index.html")
    sys.exit(1)

# 2. Inject JSON variable at the top
script_injection = f"""
  <script>
    window.normalizedLocations = {json_str};
  </script>
</head>"""

html = html.replace("</head>", script_injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html modificado exitosamente.")
