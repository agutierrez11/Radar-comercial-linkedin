import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix CSS height of #gis-map-container
css_fix = """
    #gis-map-container {
      width: 100%;
      height: 420px !important;
      border-radius: 10px;
      border: 1px solid var(--border2);
      overflow: hidden;
      background: #111827;
    }
"""

if "#gis-map-container {" in html:
    html = re.sub(r'#gis-map-container\s*\{[^}]*\}', css_fix.strip(), html)
else:
    html = html.replace('</style>', f'{css_fix}\n  </style>')

# 2. Add COUNTRY_COORDS_JS and getCoordsForContact helper before buildContacts
js_helpers = """
const COUNTRY_COORDS_JS = {
  "México": { lat: 23.6345, lng: -102.5528 },
  "Colombia": { lat: 4.5709, lng: -74.2973 },
  "Argentina": { lat: -38.4161, lng: -63.6167 },
  "Chile": { lat: -35.6751, lng: -71.5430 },
  "Brasil": { lat: -14.2350, lng: -51.9253 },
  "Estados Unidos": { lat: 37.0902, lng: -95.7129 },
  "Perú": { lat: -9.1900, lng: -75.0152 },
  "Ecuador": { lat: -1.8312, lng: -78.1834 },
  "Uruguay": { lat: -32.5228, lng: -55.7658 },
  "España": { lat: 40.4637, lng: -3.7492 },
  "Reino Unido": { lat: 55.3781, lng: -3.4360 },
  "Alemania": { lat: 51.1657, lng: 10.4515 },
  "Francia": { lat: 46.2276, lng: 2.2137 },
  "Italia": { lat: 41.8719, lng: 12.5674 },
  "Países Bajos": { lat: 52.1326, lng: 5.2913 },
  "Suiza": { lat: 46.8182, lng: 8.2275 },
  "Suecia": { lat: 60.1282, lng: 18.6435 },
  "Portugal": { lat: 39.3999, lng: -8.2245 },
  "Irlanda": { lat: 53.4129, lng: -8.2439 },
  "Bélgica": { lat: 50.5039, lng: 4.4699 },
  "Austria": { lat: 47.5162, lng: 14.5501 },
  "Polonia": { lat: 51.9194, lng: 19.1451 },
  "India": { lat: 20.5937, lng: 78.9629 },
  "Pakistán": { lat: 30.3753, lng: 69.3451 }
};

function getCoordsForContact(country, company, position) {
  const compClean = norm(company);
  const posClean = norm(position);
  const fullText = `${compClean} ${posClean}`;

  let inferredCountry = country;
  let inferredCity = 'Ciudad';

  if (!inferredCountry || inferredCountry === 'Desconocido') {
    if (fullText.includes('mexico') || fullText.includes('cdmx') || fullText.includes('cancun') || fullText.includes('monterrey')) {
      inferredCountry = 'México'; inferredCity = fullText.includes('cancun') ? 'Cancún' : 'CDMX';
    } else if (fullText.includes('colombia') || fullText.includes('bogota') || fullText.includes('medellin')) {
      inferredCountry = 'Colombia'; inferredCity = 'Bogotá';
    } else if (fullText.includes('argentina') || fullText.includes('buenos aires')) {
      inferredCountry = 'Argentina'; inferredCity = 'Buenos Aires';
    } else if (fullText.includes('chile') || fullText.includes('santiago')) {
      inferredCountry = 'Chile'; inferredCity = 'Santiago';
    } else if (fullText.includes('espana') || fullText.includes('spain') || fullText.includes('madrid') || fullText.includes('barcelona')) {
      inferredCountry = 'España'; inferredCity = fullText.includes('barcelona') ? 'Barcelona' : 'Madrid';
    } else if (fullText.includes('uk') || fullText.includes('united kingdom') || fullText.includes('london') || fullText.includes('londres')) {
      inferredCountry = 'Reino Unido'; inferredCity = 'Londres';
    } else if (fullText.includes('germany') || fullText.includes('alemania') || fullText.includes('berlin') || fullText.includes('munich')) {
      inferredCountry = 'Alemania'; inferredCity = 'Berlín';
    } else if (fullText.includes('france') || fullText.includes('francia') || fullText.includes('paris')) {
      inferredCountry = 'Francia'; inferredCity = 'París';
    } else if (fullText.includes('italy') || fullText.includes('italia') || fullText.includes('milan') || fullText.includes('rome')) {
      inferredCountry = 'Italia'; inferredCity = 'Milán';
    } else if (fullText.includes('netherlands') || fullText.includes('amsterdam')) {
      inferredCountry = 'Países Bajos'; inferredCity = 'Ámsterdam';
    } else if (fullText.includes('switzerland') || fullText.includes('suiza') || fullText.includes('zurich')) {
      inferredCountry = 'Suiza'; inferredCity = 'Zúrich';
    } else if (fullText.includes('sweden') || fullText.includes('suecia') || fullText.includes('stockholm')) {
      inferredCountry = 'Suecia'; inferredCity = 'Estocolmo';
    } else if (fullText.includes('portugal') || fullText.includes('lisbon') || fullText.includes('lisboa')) {
      inferredCountry = 'Portugal'; inferredCity = 'Lisboa';
    } else if (fullText.includes('ireland') || fullText.includes('dublin')) {
      inferredCountry = 'Irlanda'; inferredCity = 'Dublín';
    } else if (fullText.includes('us') || fullText.includes('usa') || fullText.includes('united states') || fullText.includes('miami')) {
      inferredCountry = 'Estados Unidos'; inferredCity = 'Miami';
    }
  }

  if (inferredCountry && COUNTRY_COORDS_JS[inferredCountry]) {
    return {
      country: inferredCountry,
      city: inferredCity,
      lat: COUNTRY_COORDS_JS[inferredCountry].lat,
      lng: COUNTRY_COORDS_JS[inferredCountry].lng
    };
  }

  return { country: inferredCountry || 'Desconocido', city: 'Desconocido', lat: 19.4326, lng: -99.1332 };
}
"""

# Reemplazar buildContacts con la versión corregida que asigna lat y lng a CADA contacto
new_build_contacts = """
""" + js_helpers + """
function buildContacts(rows) {
  if (S.isDemoLoaded) {
    S.contacts = [];
    S.isDemoLoaded = false;
  }

  const existingKeys = new Set(S.contacts.map(c => 
    `${norm(c.name)}|${norm(c.company)}|${norm(c.position)}|${c.connectedOn}`
  ));

  const newContacts = rows.map(row => {
    const fn = (row['First Name'] || '').trim();
    const ln = (row['Last Name'] || '').trim();
    const name = `${fn} ${ln}`.trim();
    const company = (row['Company'] || '').trim();
    const position = (row['Position'] || '').trim();
    const email = (row['Email Address'] || '').trim();
    const url = (row['URL'] || '').trim();
    const connectedOn = (row['Connected On'] || '').trim();
    const yearsAgo = connectedYearsAgo(connectedOn);
    
    const initialCountry = inferCountry(email, company, position);
    const coords = getCoordsForContact(initialCountry, company, position);
    const hierarchy = inferHierarchy(position);
    const sector = inferSector(position, company);

    let jobStatus = "🟢 Vigente Confirmado";
    if (connectedOn.includes("2025") || connectedOn.includes("2024")) {
      jobStatus = "🟡 Vigente Probable";
    } else if (connectedOn && !connectedOn.includes("2026")) {
      jobStatus = "🔍 Por Corroborar";
    }
    if (!company) jobStatus = "⚠️ Sin Empresa Registrada";

    return {
      name, company, position, originalName: name, originalCompany: company, originalPosition: position,
      email, url, connectedOn, connectedYearsAgo: yearsAgo,
      country: coords.country, city: coords.city, lat: coords.lat, lng: coords.lng,
      jobStatus, hierarchy, sector, score: 0
    };
  }).filter(c => {
    if (c.name.length === 0) return false;
    const key = `${norm(c.name)}|${norm(c.company)}|${norm(c.position)}|${c.connectedOn}`;
    if (existingKeys.has(key)) return false;
    existingKeys.add(key);
    return true;
  });

  newContacts.forEach((c, idx) => {
    c.id = S.contacts.length + idx;
  });

  S.contacts = S.contacts.concat(newContacts);
}
"""

html = re.sub(r'function buildContacts\(rows\)\s*\{[\s\S]*?\n\}', new_build_contacts.strip(), html)

# 3. Fix Leaflet noWrap tile layer options in initGisMap
old_leaflet_init = r"if \(!gisMap\) \{[\s\S]*?gisLayerGroup = L\.layerGroup\(\)\.addTo\(gisMap\);"
new_leaflet_init = """if (!gisMap) {
    gisMap = L.map('gis-map-container', {
      center: [20, -10],
      zoom: 2,
      minZoom: 2,
      maxZoom: 10,
      zoomControl: true,
      worldCopyJump: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; CARTO &copy; OpenStreetMap',
      subdomains: 'abcd',
      noWrap: true,
      bounds: [[-90, -180], [90, 180]]
    }).addTo(gisMap);

    gisLayerGroup = L.layerGroup().addTo(gisMap);
  }"""

html = re.sub(old_leaflet_init, new_leaflet_init, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Mapa corregido con altura 420px, noWrap sin repetición horizontal, y geolocalización automática de lat/lng para contactos subidos.")
