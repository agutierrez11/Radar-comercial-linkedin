"""
patch_loader_v2.py
Reemplaza el bloque SUPABASE LIVE DATA LOADER con la version v2
que es 100% compatible con la estructura interna del dashboard.
"""

NEW_LOADER = '''<script>
// ── SUPABASE LIVE DATA LOADER v2 ────────────────────────────────────────────
// Carga contactos de 'connections' en Supabase y los inyecta en S.contacts
(function() {
  var SUPA_URL = "https://hsrseeqhdtogpdqbveay.supabase.co";
  var SUPA_KEY = "sb_publishable_CeImc3_1L9K7bOTvIBKxvQ_yLRRfYmi";

  function mapRow(row, idx) {
    var m = row.metadata || {};
    var fn = (row.first_name || '').trim();
    var ln = (row.last_name || '').trim();
    var name = fn ? (fn + ' ' + ln).trim() : (m.full_name || '');
    var company = row.current_company || '';
    var position = row.current_position || '';
    var connectedOn = m.connected_on || '';
    var jobStatus = m.job_status || '\\u{1F50D} Por Corroborar';
    var lat = (m.lat !== undefined ? m.lat : 19.4326);
    var lng = (m.lng !== undefined ? m.lng : -99.1332);
    var country = m.country || 'Desconocido';
    var city = m.city || 'Desconocido';
    return {
      id: row.id || idx,
      name: name,
      first_name: fn,
      last_name: ln,
      originalName: name,
      company: company,
      originalCompany: company,
      position: position,
      originalPosition: position,
      email: row.email || '',
      url: row.linkedin_url || '',
      connectedOn: connectedOn,
      connected_on: connectedOn,
      connectedYearsAgo: 0,
      country: country,
      city: city,
      lat: lat,
      lng: lng,
      jobStatus: jobStatus,
      job_status: jobStatus,
      hierarchy: m.hierarchy || '',
      sector: m.sector || '',
      score: m.score || 0,
      audit_status: m.audit_status || 'Desconocido',
      last_post_date: m.last_post_date || '',
      last_post_text: m.last_post_text || '',
      sentiment: m.sentiment || '',
      intent: m.intent || 'Sin Contacto',
      has_reply: m.has_reply || false,
      is_deal: m.is_deal || false,
      turns: m.turns || 0,
      direction: m.direction || 'Sin Conversacion',
      is_they_selling: m.is_they_selling || false,
      is_friendly: m.is_friendly || false,
      msg_count: m.msg_count || 0,
      crmStatus: m.crmStatus || 'Ninguno',
      crmNotes: m.crmNotes || '',
      is_current: (jobStatus.indexOf('Vigente') !== -1),
    };
  }

  async function fetchAllConnections(supaClient) {
    var allRows = [];
    var from = 0;
    var BATCH = 1000;
    var more = true;
    while (more) {
      var result = await supaClient
        .from("connections")
        .select("*")
        .range(from, from + BATCH - 1);
      if (result.error) { console.error("[Supabase] Error:", result.error.message); break; }
      if (!result.data || result.data.length === 0) { more = false; break; }
      allRows = allRows.concat(result.data);
      from += BATCH;
      if (result.data.length < BATCH) { more = false; }
    }
    return allRows;
  }

  window.__supabaseDataPromise = new Promise(function(resolve) {
    document.addEventListener("DOMContentLoaded", function() {
      var bar = document.getElementById("loading-bar");
      var fill = document.getElementById("loading-fill");
      if (bar) bar.style.display = "block";
      if (fill) fill.style.width = "15%";

      if (!window.supabase || typeof window.supabase.createClient !== 'function') {
        console.error("[Supabase] SDK no disponible. Comprobando cdn...");
        resolve([]);
        return;
      }

      var supaClient = window.supabase.createClient(SUPA_URL, SUPA_KEY);
      if (fill) fill.style.width = "40%";

      fetchAllConnections(supaClient).then(function(rows) {
        console.log("[Supabase] Filas recibidas:", rows.length);
        if (fill) fill.style.width = "85%";
        var mapped = rows.map(mapRow);
        window.ENRICHED_CONNECTIONS_DATA = mapped;
        if (fill) fill.style.width = "100%";
        setTimeout(function() { if (bar) bar.style.display = "none"; }, 500);
        resolve(mapped);
      }).catch(function(e) {
        console.error("[Supabase] Error al fetchear:", e);
        window.ENRICHED_CONNECTIONS_DATA = [];
        if (bar) bar.style.display = "none";
        resolve([]);
      });
    });
  });
})();
</script>'''

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Marker de inicio del bloque viejo
START_MARKER = "<script>\n// ── SUPABASE LIVE DATA LOADER ──"
END_MARKER = "\n</script>"

start_idx = content.find(START_MARKER)
if start_idx == -1:
    # Try CRLF
    START_MARKER = "<script>\r\n// ── SUPABASE LIVE DATA LOADER ──"
    start_idx = content.find(START_MARKER)

if start_idx == -1:
    print("[ERROR] No se encontro el marcador de inicio del loader viejo")
    print("Buscando alternativa...")
    start_idx = content.find("// ── SUPABASE LIVE DATA LOADER")
    if start_idx > 0:
        # Retroceder para incluir el <script>
        tag_start = content.rfind("<script>", 0, start_idx)
        if tag_start > 0:
            start_idx = tag_start
            print(f"[OK] Encontrado en posicion {start_idx}")
else:
    print(f"[OK] Marcador encontrado en posicion {start_idx}")

if start_idx == -1:
    print("[FAIL] No se pudo localizar el bloque. Abortando.")
else:
    # Encontrar el cierre </script> despues del inicio
    end_idx = content.find("</script>", start_idx) + len("</script>")
    old_block = content[start_idx:end_idx]
    print(f"[INFO] Bloque viejo ({len(old_block)} bytes):")
    print(old_block[:200], "...")
    
    content = content[:start_idx] + NEW_LOADER + content[end_idx:]
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[DONE] Loader v2 inyectado. Nuevo tamano: {len(content.encode('utf-8')) // 1024} KB")
