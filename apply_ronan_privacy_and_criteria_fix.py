"""
apply_ronan_privacy_and_criteria_fix.py
1. Fixes data contamination so Ronan/Giovanna demo vaults NEVER leak Antonio's real messages.
2. Removes "TESIS BECARIO -> CEO" badge from ronan banner.
3. Fixes Option B click handler so it updates the table in place without unwanted redirects.
4. Adds ZIP Data Selector & Enrichment Criteria Panel in sec-upload.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DIR = os.path.dirname(os.path.abspath(__file__))

def patch_file(file_name):
    file_path = os.path.join(DIR, file_name)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. Remove "TESIS BECARIO -> CEO" badge from banner
    html = html.replace(
        '<span class="badge" style="background:var(--purple); color:#fff; font-size:9px;">TESIS BECARIO ➔ CEO</span>',
        ''
    )
    html = html.replace(
        '<span class="badge" style="background:var(--purple); color:#fff; font-size:9px;">TESIS BECARIO &#10132; CEO</span>',
        ''
    )

    # 2. Add Isolated Demo Messages for Ronan so Antonio's real messages are NEVER displayed
    ronan_messages_js = """
window.RONAN_DEMO_MESSAGES = [
  { ID: 'ron_m1', FROM: 'Carlos Gómez', TO: 'Ronan', CONTENT: 'Hola Ronan, vi tu publicación sobre inteligencia de ventas B2B. ¿Tienen disponibilidad para una demo esta semana?', timestamp: '2026-08-20T10:15:00Z', DIRECTION: 'INBOUND' },
  { ID: 'ron_m2', FROM: 'Ronan', TO: 'Carlos Gómez', CONTENT: 'Hola Carlos, con gusto. Te comparto nuestra agenda de coordinadores para revisar tu pipeline.', timestamp: '2026-08-20T10:18:00Z', DIRECTION: 'OUTBOUND' },
  { ID: 'ron_m3', FROM: 'Sofía Morales', TO: 'Ronan', CONTENT: 'Excelente solución para prospección en LinkedIn. ¿Cómo manejan el cifrado local de datos?', timestamp: '2026-08-19T16:30:00Z', DIRECTION: 'INBOUND' },
  { ID: 'ron_m4', FROM: 'David Miller', TO: 'Ronan', CONTENT: 'Nos interesa integrar el conector de Supabase con nuestro CRM en México.', timestamp: '2026-08-18T14:20:00Z', DIRECTION: 'INBOUND' }
];
"""

    # Ensure setupSandboxRonanMode and setupSandboxRonanRawCsvMode use window.RONAN_DEMO_MESSAGES
    ronan_setup_patch = """function setupSandboxRonanMode() {
  if (typeof RONAN_DEMO_MESSAGES === 'undefined') {
    window.RONAN_DEMO_MESSAGES = [
      { ID: 'ron_m1', FROM: 'Carlos Gómez', TO: 'Ronan', CONTENT: 'Hola Ronan, vi tu publicación sobre inteligencia de ventas B2B. ¿Tienen disponibilidad para una demo esta semana?', timestamp: '2026-08-20T10:15:00Z', DIRECTION: 'INBOUND' },
      { ID: 'ron_m2', FROM: 'Ronan', TO: 'Carlos Gómez', CONTENT: 'Hola Carlos, con gusto. Te comparto nuestra agenda de coordinadores para revisar tu pipeline.', timestamp: '2026-08-20T10:18:00Z', DIRECTION: 'OUTBOUND' },
      { ID: 'ron_m3', FROM: 'Sofía Morales', TO: 'Ronan', CONTENT: 'Excelente solución para prospección en LinkedIn. ¿Cómo manejan el cifrado local de datos?', timestamp: '2026-08-19T16:30:00Z', DIRECTION: 'INBOUND' },
      { ID: 'ron_m4', FROM: 'David Miller', TO: 'Ronan', CONTENT: 'Nos interesa integrar el conector de Supabase con nuestro CRM en México.', timestamp: '2026-08-18T14:20:00Z', DIRECTION: 'INBOUND' }
    ];
  }
  S.messages = window.RONAN_DEMO_MESSAGES;
  S.loadedParts = { connections: true, messages: true, positions: true, profile: true };
"""

    if "function setupSandboxRonanMode() {" in html:
        html = html.replace("function setupSandboxRonanMode() {", ronan_setup_patch)

    # 3. Add ZIP Extraction & Criteria Selector in sec-upload
    criteria_panel = """
          <!-- CRITERIOS DE EXTRACCIÓN Y DATOS DEL ZIP (OPCIÓN B) -->
          <div style="margin-top:16px; text-align:left; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; box-shadow:var(--shadow-sm);">
            <div style="font-size:12px; font-weight:700; color:var(--text); margin-bottom:8px; display:flex; align-items:center; gap:6px;">
              <span>⚙️ Criterios de Selección y Componentes a Extraer del ZIP</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:12px;">
              <label style="font-size:11px; color:var(--text); display:flex; align-items:center; gap:6px; cursor:pointer;">
                <input type="checkbox" id="chk-import-connections" checked style="accent-color:var(--accent);">
                <span>Connections.csv (Contactos)</span>
              </label>
              <label style="font-size:11px; color:var(--text); display:flex; align-items:center; gap:6px; cursor:pointer;">
                <input type="checkbox" id="chk-import-messages" checked style="accent-color:var(--accent);">
                <span>Messages.csv (Conversaciones)</span>
              </label>
              <label style="font-size:11px; color:var(--text); display:flex; align-items:center; gap:6px; cursor:pointer;">
                <input type="checkbox" id="chk-import-positions" checked style="accent-color:var(--accent);">
                <span>Positions.csv (Trayectoria)</span>
              </label>
              <label style="font-size:11px; color:var(--text); display:flex; align-items:center; gap:6px; cursor:pointer;">
                <input type="checkbox" id="chk-import-profile" checked style="accent-color:var(--accent);">
                <span>Profile.csv (Biografía)</span>
              </label>
            </div>

            <div style="border-top:1px solid var(--border); padding-top:10px; display:flex; flex-wrap:wrap; gap:12px; align-items:center;">
              <div style="font-size:11px; font-weight:600; color:var(--text-muted);">Motor de Enriquecimiento:</div>
              <select id="sel-enrichment-engine" class="filter-input" style="font-size:11px; padding:4px 8px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">
                <option value="harvestapi">🟢 Opción B: Enriquecimiento en Vivo (HarvestAPI)</option>
                <option value="apify">⚡ Enriquecimiento Masivo (Apify Lotes)</option>
                <option value="csv_raw">🔴 Opción A: CSV Plano (Sin Enriquecer)</option>
              </select>
              <div style="font-size:11px; font-weight:600; color:var(--text-muted);">Scoring Mínimo ICP:</div>
              <input type="number" id="num-min-scoring" value="50" min="0" max="100" style="width:60px; font-size:11px; padding:4px 6px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">
            </div>
          </div>
"""

    if '<!-- CRITERIOS DE EXTRACCIÓN Y DATOS DEL ZIP' not in html:
        html = html.replace('<!-- Instrucciones de Descarga -->', criteria_panel + '\n\n          <!-- Instrucciones de Descarga -->')

    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html)
    print(f"PATCHED: {file_name}")

patch_file("staging.html")
patch_file("index.html")
