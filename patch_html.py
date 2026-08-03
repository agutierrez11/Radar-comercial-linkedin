"""
patch_html.py
Inyecta la capa de Supabase en index.html:
1. Agrega el SDK de Supabase antes del cierre de </head>
2. Reemplaza el bloque <script> hardcodeado de datos (linea 441-442)
   con un loader async que llama a Supabase y puebla la misma variable.
"""
import re

SUPABASE_URL = "https://hsrseeqhdtogpdqbveay.supabase.co"
SUPABASE_ANON = "sb_publishable_CeImc3_1L9K7bOTvIBKxvQ_yLRRfYmi"

HTML_FILE = "index.html"

with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Inyectar SDK de Supabase en <head> ───────────────────────────────────
SDK_SCRIPT = '''  <!-- Supabase SDK -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
'''
if "supabase.js" not in content:
    content = content.replace("</head>", SDK_SCRIPT + "</head>", 1)
    print("[OK] SDK de Supabase inyectado en <head>")
else:
    print("[SKIP] SDK ya presente")

# ── 2. Reemplazar el bloque de datos hardcodeado ────────────────────────────
LOADER_BLOCK = f"""<script>
// ── SUPABASE LIVE DATA LOADER ──────────────────────────────────────────────
// Reemplaza el JSON estatico. Carga los 3,039 contactos desde Supabase
// en lotes de 1000 (limite de Supabase por request) y llama a initDashboard()
// cuando todo esta listo.
(function() {{
  const SUPA_URL = "{SUPABASE_URL}";
  const SUPA_KEY = "{SUPABASE_ANON}";

  // Pantalla de carga
  document.addEventListener("DOMContentLoaded", function() {{
    var loadingBar = document.getElementById("loading-bar");
    var loadingFill = document.getElementById("loading-fill");
    if (loadingBar) {{ loadingBar.style.display = "block"; }}
    if (loadingFill) {{ loadingFill.style.width = "20%"; }}
  }});

  async function fetchAllConnections() {{
    const supabase = window.supabase.createClient(SUPA_URL, SUPA_KEY);
    let allRows = [];
    let from = 0;
    const BATCH = 1000;
    let more = true;

    while (more) {{
      const {{ data, error }} = await supabase
        .from("connections")
        .select("*")
        .range(from, from + BATCH - 1);
      if (error) {{ console.error("[Supabase] Error:", error); break; }}
      if (!data || data.length === 0) {{ more = false; break; }}
      allRows = allRows.concat(data);
      from += BATCH;
      if (data.length < BATCH) {{ more = false; }}
    }}
    return allRows;
  }}

  function mapRow(row) {{
    const m = row.metadata || {{}};
    return {{
      id: row.id,
      first_name: row.first_name || "",
      last_name: row.last_name || "",
      full_name: m.full_name || (row.first_name + " " + row.last_name).trim(),
      url: row.linkedin_url || "",
      connected_on: m.connected_on || "",
      company: row.current_company || "",
      position: row.current_position || "",
      company_zip: row.current_company || "",
      position_zip: row.current_position || "",
      audit_status: m.audit_status || "Desconocido",
      job_status: m.job_status || "Sin estado",
      last_updated_apify: m.last_updated_apify || "",
      last_post_date: m.last_post_date || "",
      last_post_text: m.last_post_text || "",
      position_current: row.current_position || "",
      sentiment: m.sentiment || "",
      intent: m.intent || "Sin Contacto",
      has_reply: m.has_reply || false,
      is_deal: m.is_deal || false,
      turns: m.turns || 0,
      direction: m.direction || "Sin Conversacion",
      sentiment_detail: m.sentiment || "",
      is_they_selling: m.is_they_selling || false,
      is_friendly: m.is_friendly || false,
      country: "Desconocido",
      city: "Desconocido",
      lat: 19.4326,
      lng: -99.1332,
      is_current: (m.job_status || "").includes("Vigente"),
    }};
  }}

  // Registrar la promesa de carga para que initDashboard espere
  window.__supabaseDataPromise = fetchAllConnections().then(function(rows) {{
    console.log("[Supabase] Contactos cargados:", rows.length);
    window.ENRICHED_CONNECTIONS_DATA = rows.map(mapRow);

    // Actualizar barra de progreso
    var loadingFill = document.getElementById("loading-fill");
    if (loadingFill) {{ loadingFill.style.width = "100%"; }}
    setTimeout(function() {{
      var loadingBar = document.getElementById("loading-bar");
      if (loadingBar) {{ loadingBar.style.display = "none"; }}
    }}, 400);

    return window.ENRICHED_CONNECTIONS_DATA;
  }}).catch(function(e) {{
    console.error("[Supabase] Fallo critico al cargar datos:", e);
    window.ENRICHED_CONNECTIONS_DATA = [];
  }});
}})();
</script>"""

# Detectar el bloque del script hardcodeado (empieza exactamente con esta cadena)
OLD_MARKER = "<script>\nwindow.ENRICHED_CONNECTIONS_DATA = ["
if OLD_MARKER not in content:
    # Intentar con \r\n
    OLD_MARKER = "<script>\r\nwindow.ENRICHED_CONNECTIONS_DATA = ["

if OLD_MARKER in content:
    # Encontrar el cierre del bloque: la primera ocurrencia de </script> despues del marker
    start_idx = content.index(OLD_MARKER)
    end_idx = content.index("</script>", start_idx) + len("</script>")
    content = content[:start_idx] + LOADER_BLOCK + content[end_idx:]
    print("[OK] Bloque de datos estaticos reemplazado por loader de Supabase")
else:
    print("[ERROR] No se encontro el marcador del bloque de datos. Verificar manualmente.")

# ── 3. Guardar ───────────────────────────────────────────────────────────────
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)
print("[DONE] index.html actualizado correctamente.")
print(f"Nuevo size: {len(content.encode('utf-8')) // 1024} KB")
