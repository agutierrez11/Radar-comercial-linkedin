import re

def fix_html_sections(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find main content start
    main_match = re.search(r'<main id="main-content">', content)
    if not main_match:
        print(f"Error: main tag not found in {filepath}")
        return

    main_start = main_match.end()

    # Find sec-profile start
    profile_match = re.search(r'<!-- ── PROFILE ── -->\s*<div class="section" id="sec-profile">', content)
    if not profile_match:
        profile_match = re.search(r'<div class="section" id="sec-profile">', content)
    
    profile_start = profile_match.start()

    # Everything between <main id="main-content"> and <div class="section" id="sec-profile"> needs clean reconstruction:
    # 1. sec-upload
    # 2. sec-network (containing A/B bar + vault-view-container-a + vault-view-container-b)

    # Extract original upload section inner content
    upload_inner_match = re.search(r'<div id="upload-screen">[\s\S]*?</div>\s*</div>\s*</div>', content[main_start:profile_start])
    
    # If not found cleanly, extract from drop-zone to status card
    upload_html = """
    <!-- ── UPLOAD ── -->
    <div class="section" id="sec-upload">
      <div id="upload-screen">
        <div class="upload-card">
          <div class="upload-icon">🗜️</div>
          <h2>Comienza a minar tu red</h2>
          <p>Sube tus archivos de exportación de LinkedIn.<br>Puedes subir varios ZIPs o CSVs (ej: si LinkedIn dividió tu descarga en 2 ZIPs). Todo local.</p>
          <div class="upload-zone" id="drop-zone" onclick="document.getElementById('zip-input').click()">
            <p style="font-size:13px;font-weight:600;margin-bottom:4px">Arrastra tus archivos aquí</p>
            <p style="font-size:11px;color:var(--muted)">ZIP completo o CSVs individuales (puedes seleccionar varios)</p>
            <input type="file" id="zip-input" accept=".zip,.csv" style="display:none" multiple>
          </div>
          <div style="display:flex; gap:12px; justify-content:center; margin-bottom:12px; flex-wrap:wrap;">
            <button class="upload-btn" onclick="document.getElementById('zip-input').click()">
              📁 Seleccionar archivos
            </button>
            <button class="upload-btn" style="background:var(--surface); color:var(--text); border:1px solid var(--border);" onclick="loadDemoData()">
              🚀 Cargar datos de prueba
            </button>
          </div>
          
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

          <div style="margin-top:20px; text-align:left; background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:15px;">
            <h4 style="font-size:11px; margin-bottom:10px; color:var(--text); display:flex; align-items:center; gap:6px;">
              <span style="font-size:14px;">ℹ️</span> ¿Cómo obtengo mi ZIP de LinkedIn?
            </h4>
            <ol style="font-size:11px; color:var(--muted2); margin-left:20px; line-height:1.6; padding-left:4px; margin-top:0;">
              <li style="margin-bottom:6px;">En LinkedIn, haz clic en el icono <strong>Yo</strong> (arriba a la derecha) y selecciona <strong>Ajustes y privacidad</strong>.</li>
              <li style="margin-bottom:6px;">En el menú izquierdo, ve a <strong>Privacidad de datos</strong> y luego a <strong>Obtener una copia de tus datos</strong>.</li>
              <li style="margin-bottom:6px;">Elige la opción <em>"Descarga un archivo de datos más grande..."</em> y presiona <strong>Solicitar archivo</strong>.</li>
            </ol>
            <p style="font-size:10px; color:var(--muted); margin-top:8px; margin-bottom:12px; font-style:italic;">* LinkedIn te enviará un correo cuando tu ZIP esté listo para descargar.</p>
            
            <details style="font-size:11px; color:var(--text); cursor:pointer;">
              <summary style="font-weight:600; outline:none; margin-bottom:4px;">🎥 Ver video tutorial (1 min)</summary>
              <video width="100%" controls preload="metadata" style="border-radius:8px; border:1px solid var(--border); margin-top:8px; box-shadow: var(--shadow-sm);">
                <source src="tutorial_exportacion_web.mp4" type="video/mp4">
                Tu navegador no soporta reproducción de video.
              </video>
            </details>
          </div>
          
          <div class="upload-status-card" id="upload-status" style="display:none; margin-top:20px; text-align:left; background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:15px;">
            <h4 style="font-size:10px; margin-bottom:10px; color:var(--muted2); font-family:'JetBrains Mono', monospace; text-transform:uppercase; letter-spacing:0.05em;">Componentes Importados:</h4>
            <div style="display:flex; flex-direction:column; gap:8px;">
              <div id="status-connections" style="display:flex; align-items:center; gap:8px; font-size:11px;">
                <span class="status-dot" style="width:8px; height:8px; border-radius:50%; background:var(--muted); flex-shrink:0;"></span>
                <span class="status-label">Contactos (Connections.csv): <strong style="color:var(--muted)">Pendiente</strong></span>
              </div>
              <div id="status-messages" style="display:flex; align-items:center; gap:8px; font-size:11px;">
                <span class="status-dot" style="width:8px; height:8px; border-radius:50%; background:var(--muted); flex-shrink:0;"></span>
                <span class="status-label">Mensajes (messages.csv): <strong style="color:var(--muted)">Pendiente</strong></span>
              </div>
              <div id="status-positions" style="display:flex; align-items:center; gap:8px; font-size:11px;">
                <span class="status-dot" style="width:8px; height:8px; border-radius:50%; background:var(--muted); flex-shrink:0;"></span>
                <span class="status-label">Cargos (Positions.csv): <strong style="color:var(--muted)">Pendiente</strong></span>
              </div>
            </div>
            <div style="margin-top:15px; display:flex; gap:8px;">
              <button class="mini-btn primary" id="btn-go-dashboard" style="flex:1; display:none;" onclick="navigate('network')">Ver Dashboard →</button>
              <button class="mini-btn" id="btn-reset-data" style="flex:1;" onclick="resetAllData()">Limpiar</button>
            </div>
          </div>

          <div class="upload-hint">
            💡 ¿Cómo exportar? <a href="https://www.linkedin.com/psettings/member-data" target="_blank">Configuración de datos de LinkedIn ↗</a><br>
            <span style="color:var(--muted)">Marca "Mis contactos" y solicita el archivo completo. Si pesa mucho, te darán 2 partes.</span>
          </div>
        </div>
      </div>
    </div>
"""

    # Extract Vista A content (from section-header of Mi Red to end of table/gis)
    vista_a_match = re.search(r'<div class="section-header">\s*<div><div class="section-title">🌐 Mi Red de Contactos</div>[\s\S]*?(?=<!-- ── VISTA B:|$)', content[main_start:profile_start])
    
    # If vista a is inside vault-view-container-a, let's extract inner container a
    container_a_match = re.search(r'<div id="vault-view-container-a">([\s\S]*?)</div>\s*<div class="section-header">', content[main_start:profile_start])
    if not container_a_match:
        container_a_match = re.search(r'<div id="vault-view-container-a">([\s\S]*?)(?=<!-- ── VISTA B:|<div id="vault-view-container-b">)', content[main_start:profile_start])

    container_b_match = re.search(r'<div id="vault-view-container-b"[\s\S]*?</div>\s*</div>\s*(?=<!-- ── PROFILE ── -->|<div class="section" id="sec-profile">)', content[main_start:profile_start])
    if not container_b_match:
        container_b_match = re.search(r'<div id="vault-view-container-b"[\s\S]*?</div>\s*</div>', content)

    # Build clean sec-network HTML
    network_html = """
    <!-- ── NETWORK ── -->
    <div class="section active" id="sec-network">

      <!-- ── A/B TOGGLE BAR DE NAVEGACIÓN EN BÓVEDA ── -->
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:10px 16px; flex-wrap:wrap; gap:10px; box-shadow:var(--shadow-sm);">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:12px; font-weight:700; color:var(--text); font-family:'Outfit',sans-serif;">🎛️ Experiencia de Bóveda:</span>
          <span style="font-size:11px; color:var(--text-muted);">Selecciona la interfaz preferida para tu equipo</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px; background:var(--bg); padding:4px; border-radius:8px; border:1px solid var(--border);">
          <button class="mini-btn active" id="vault-mode-btn-a" onclick="switchVaultViewMode('A')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            📊 Vista A: Clásica (Dashboard & Mapa GIS)
          </button>
          <button class="mini-btn" id="vault-mode-btn-b" onclick="switchVaultViewMode('B')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; cursor:pointer; transition:all 0.2s;">
            ✨ Vista B: Bóveda B2B Pro (Attio / Linear)
          </button>
        </div>
      </div>

      <!-- ── VISTA A: CLÁSICA BI & MAPA GIS ── -->
      <div id="vault-view-container-a">
        <div class="section-header">
          <div><div class="section-title">🌐 Mi Red de Contactos</div><div class="section-sub">Análisis por jerarquía, país y sector</div></div>
          <button class="mini-btn" onclick="exportCSV(filteredContacts, 'red_contactos')">↓ Exportar CSV</button>
        </div>

        <!-- BANNER PRUEBA A/B RONAN BI TEST -->
        <div id="ronan-ab-banner" style="display:none; background:linear-gradient(135deg, rgba(79,70,229,0.18), rgba(124,58,237,0.18)); border:1px solid var(--accent); border-radius:12px; padding:14px 18px; margin-bottom:16px; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <div>
            <div style="font-size:13px; font-weight:800; color:var(--accent); font-family:'Outfit',sans-serif; display:flex; align-items:center; gap:8px;">
              <span>🧪 MÓDULO DE VALIDACIÓN BI / PRUEBA A/B (DEMO RONAN)</span>
            </div>
            <div style="font-size:11px; color:var(--text-muted); margin-top:3px; max-width:650px;" id="ronan-ab-explainer">
              🟢 <b>Opción B (Enriquecida en Vivo 2026):</b> Muestra la red viva con HarvestAPI + IA. Revela los cargos actuales (CEOs, VPs) de contactos que eran analistas en 2018.
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px; background:var(--bg); padding:4px 6px; border-radius:8px; border:1px solid var(--border);">
            <button class="mini-btn" id="ab-btn-option-a" onclick="switchRonanAbMode('A')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; background:transparent; color:var(--text-muted); border:1px solid var(--border); cursor:pointer;">
              🔴 Opción A: CSV Plano (Sin Enriquecer)
            </button>
            <button class="mini-btn active" id="ab-btn-option-b" onclick="switchRonanAbMode('B')" style="padding:6px 14px; font-weight:700; font-size:11px; border-radius:6px; background:var(--accent); color:#fff; border:1px solid var(--accent); cursor:pointer;">
              🟢 Opción B: Enriquecido en Vivo (2026)
            </button>
          </div>
        </div>

        <div class="kpi-row" id="net-kpis"></div>
        <div class="charts-row" id="net-charts" style="display:none">
          <div class="chart-card"><div class="chart-title">Jerarquía</div><div class="chart-canvas-wrap"><canvas id="chart-hier"></canvas></div></div>
          <div class="chart-card"><div class="chart-title">Top Países</div><div class="chart-canvas-wrap"><canvas id="chart-countries"></canvas></div></div>
        </div>
        
        <!-- 🗺️ MAPA ESPACIAL GIS (mapcn-gis-specialist) -->
        <div class="chart-card" id="map-gis-card" style="display:none; margin-bottom: 16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
            <div class="chart-title" style="display:flex; align-items:center; gap:8px;">
              <span>🗺️ Mapa Espacial de Relaciones (Warm Territory Intelligence)</span>
              <span class="badge badge-green" id="map-contact-count">0 contactos mapeados</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button class="mini-btn" onclick="resetMapZoom()" style="padding:4px 8px; font-size:11px;">🔍 Re-centrar Mapa</button>
            </div>
          </div>
          <div id="gis-map" style="width:100%; height:320px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1;"></div>
        </div>

        <!-- FILTROS & TABLA CLÁSICA -->
        <div class="filter-bar">
          <div class="filter-group" style="flex:2">
            <label>Buscar en la red</label>
            <input class="filter-input" id="search-input" type="text" placeholder="Nombre, cargo, empresa, país, ciudad..." oninput="onFilterChange()">
          </div>
          <div class="filter-group">
            <label>Jerarquía</label>
            <select class="filter-input" id="filter-hier" onchange="onFilterChange()">
              <option value="">Todas</option>
              <option value="c-level">C-Level (CEO, CTO...)</option>
              <option value="director">Director / VP</option>
              <option value="gerente">Gerente / Manager</option>
              <option value="otro">Otros cargos</option>
            </select>
          </div>
          <div class="filter-group">
            <label>País</label>
            <select class="filter-input" id="filter-country" onchange="onFilterChange()">
              <option value="">Todos los países</option>
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:12px; color:var(--text-muted);">
          <div id="table-counter">Mostrando 0 contactos</div>
          <div style="display:flex; gap:8px; align-items:center;">
            <span>Orden:</span>
            <select class="filter-input" id="sort-select" onchange="onFilterChange()" style="font-size:11px; padding:3px 8px;">
              <option value="name-asc">Nombre (A-Z)</option>
              <option value="score-desc">Mayor Scoring ICP</option>
              <option value="date-desc">Conexión reciente</option>
            </select>
          </div>
        </div>

        <div class="table-wrap">
          <table id="contacts-table">
            <thead>
              <tr>
                <th>Contacto</th>
                <th>Cargo / Posición</th>
                <th>Empresa</th>
                <th>Ubicación</th>
                <th>Fecha Conexión</th>
                <th>Score ICP</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody id="contacts-tbody"></tbody>
          </table>
        </div>
      </div><!-- END vault-view-container-a -->

      <!-- ── VISTA B: REDISEÑO B2B PRO (ATTIO / LINEAR SPEC) ── -->
      <div id="vault-view-container-b" style="display:none; font-family:'Outfit',sans-serif;">
        <!-- BÚSQUEDA HÉROE PROTAGONISTA -->
        <div style="background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:24px 20px; margin-bottom:20px; box-shadow:var(--shadow-sm);">
          <div style="text-align:center; max-width:640px; margin:0 auto 16px auto;">
            <h2 style="font-size:20px; font-weight:800; color:var(--text); margin-bottom:6px;">Explora tu Bóveda Privada de Inteligencia</h2>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.5;">Busca por nombre, cargo, empresa, palabras clave o temas de conversación en tu red.</p>
          </div>

          <div style="position:relative; max-width:720px; margin:0 auto 14px auto;">
            <input type="text" id="vault-b-search-input" class="filter-input" placeholder="🔍 Ejemplo: 'batas', 'cfo fintech', 'epp', 'pagos', 'compras hospital'..." style="width:100%; padding:14px 44px 14px 16px; font-size:14px; border-radius:10px; background:var(--bg); border:1px solid var(--accent); color:var(--text); outline:none; box-shadow:0 0 0 3px rgba(79,70,229,0.15);" onkeyup="handleVaultBSearch(event)">
            <button onclick="triggerVaultBSearch()" style="position:absolute; right:10px; top:50%; transform:translateY(-50%); background:var(--accent); color:white; border:none; border-radius:6px; padding:6px 14px; font-weight:700; font-size:12px; cursor:pointer;">Buscar</button>
          </div>

          <!-- CHIPS DE BÚSQUEDA RÁPIDA -->
          <div style="display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;">
            <span style="font-size:11px; color:var(--text-muted); font-weight:600;">Sugerencias:</span>
            <button class="mini-btn" onclick="quickSearchVaultB('hospital')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🩺 Compras Hospitales</button>
            <button class="mini-btn" onclick="quickSearchVaultB('pagos')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">💳 Payments / Fintech</button>
            <button class="mini-btn" onclick="quickSearchVaultB('epp')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🛡️ Equipos EPP</button>
            <button class="mini-btn" onclick="quickSearchVaultB('cfo')" style="padding:4px 10px; font-size:11px; border-radius:6px; background:var(--bg); border:1px solid var(--border); color:var(--text);">🎯 Decisores C-Level</button>
          </div>
        </div>

        <!-- 3 KPIS COMERCIALES NÍTIDOS -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:20px;">
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(99,102,241,0.12); color:var(--accent); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">🎯</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Perfiles de Alto ICP</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-icp">296</div>
            </div>
          </div>
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(16,185,129,0.12); color:var(--green); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">💬</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Chats a Re-contactar</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-chats">14</div>
            </div>
          </div>
          <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px; display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(245,158,11,0.12); color:var(--amber); width:42px; height:42px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px;">🚀</div>
            <div>
              <div style="font-size:11px; color:var(--text-muted); font-weight:600; text-transform:uppercase; letter-spacing:.05em;">Cuentas Objetivo Co-Selling</div>
              <div style="font-size:22px; font-weight:800; color:var(--text);" id="vb-kpi-opps">8</div>
            </div>
          </div>
        </div>

        <!-- SEGMENTACIÓN & FILTROS SOBRIOS -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button class="mini-btn active" id="vb-filter-all" onclick="filterVaultB('all')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">Todos (<span id="vb-count-total">2,953</span>)</button>
            <button class="mini-btn" id="vb-filter-clevel" onclick="filterVaultB('clevel')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">🎯 C-Level & Directores</button>
            <button class="mini-btn" id="vb-filter-chats" onclick="filterVaultB('chats')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">💬 Con Historial de Chat</button>
            <button class="mini-btn" id="vb-filter-mexico" onclick="filterVaultB('mexico')" style="padding:6px 12px; font-weight:700; font-size:11px; border-radius:6px;">🇲🇽 México</button>
          </div>
          <div style="font-size:12px; color:var(--text-muted);" id="vb-results-counter">
            Mostrando prospectos explicables de tu red
          </div>
        </div>

        <!-- FEED DE RESULTADOS EXPLICABLES ESTILO ATTIO/LINEAR -->
        <div id="vault-b-feed" style="display:flex; flex-direction:column; gap:10px;">
          <!-- Injected dynamically by renderVaultBFeed() -->
        </div>
      </div><!-- END vault-view-container-b -->

    </div><!-- END sec-network -->
"""

    new_content = content[:main_start] + upload_html + network_html + content[profile_start:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_html_sections("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
fix_html_sections("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Fixed HTML sections in index.html and staging.html!")
