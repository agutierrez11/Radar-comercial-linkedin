"""
patch_staging.py
Patches staging.html with RadarCore integration, simplified topbar dropdown,
reorganized task-based sidebar, and tabular-nums visual polish.
"""
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_PATH = os.path.join(DIR, "staging.html")

def patch_staging():
    with open(STAGING_PATH, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. Add radar_core.js script include after master_data.js if not present
    if "radar_core.js" not in html:
        html = html.replace(
            '<script src="master_data.js"></script>',
            '<script src="master_data.js"></script>\n  <script src="radar_core.js"></script>'
        )

    # 2. Add tabular-nums CSS rule
    tabular_css = """
    .tabular-nums, .kpi-pill, .nav-badge, .stat-value, .stat-card, .table-cell-num, #hkpi-total, #hkpi-clevel, #hkpi-countries {
      font-variant-numeric: tabular-nums;
    }
    """
    if ".tabular-nums" not in html:
        html = html.replace("</style>", tabular_css + "\n</style>", 1)

    # 3. Simplify Header Topbar & Add Más Dropdown
    header_old_pattern = re.compile(r'<header id="app-header">.*?</header>', re.DOTALL)
    header_new = """<header id="app-header" style="display:flex; align-items:center; gap:10px; padding:8px 16px; background:var(--surface); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:1000;">
  <div class="header-logo" style="display:flex; align-items:center; gap:8px; font-weight:800; font-size:16px; color:var(--text); cursor:pointer;" onclick="navigate('upload')">
    <div class="logo-icon" style="background:var(--accent); color:#fff; width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:14px;">📡</div>
    <div class="logo-text" style="font-family:'Outfit',sans-serif;">RADAR <span style="color:var(--accent);">COMERCIAL</span></div>
  </div>

  <!-- Search Input (Centro) -->
  <div style="flex:1; max-width:460px; margin:0 12px;">
    <input type="text" id="network-talk-search" class="filter-input" placeholder="🔍 Buscar en mi bóveda (nombre, cargo, mensajes, sinónimos...)" style="width:100%; font-size:12px; padding:6px 12px; border-radius:8px; background:var(--bg); border:1px solid var(--border); color:var(--text);" onkeyup="handleTalkToNetworkSearch(event)" title="Búsqueda explicable local-first con RadarCore">
  </div>

  <!-- KPIs Compactos -->
  <div class="header-kpis" id="header-kpis" style="display:none; gap:6px; align-items:center;">
    <div class="kpi-pill tabular-nums" style="font-size:11px; padding:3px 8px; border-radius:6px; background:rgba(16,185,129,0.1); border:1px solid var(--green); color:var(--green);"><span id="hkpi-total">0</span> cont.</div>
  </div>

  <!-- Active User Pill -->
  <div class="kpi-pill" id="active-user-pill" onclick="openLoginModal()" style="cursor:pointer !important; background:rgba(79,70,229,0.12); border:1px solid var(--accent); color:var(--text); font-weight:700; font-size:11px; padding:4px 10px; border-radius:20px; display:flex; align-items:center; gap:6px;" title="Cambiar usuario/bóveda">
    <span class="dot" style="width:7px; height:7px; border-radius:50%; background:var(--green); display:inline-block;"></span>
    <span id="active-user-name">👤 Antonio</span>
  </div>

  <!-- Botón Más Dropdown -->
  <div class="dropdown-container" style="position:relative;">
    <button class="mini-btn" id="more-menu-btn" onclick="toggleMoreMenu(event)" style="display:flex; align-items:center; gap:6px; padding:5px 12px; font-weight:600; border-radius:8px; border:1px solid var(--border); background:var(--bg); color:var(--text); cursor:pointer;">
      ⚙️ <span>Configuración / Más ▾</span>
    </button>
    <div id="more-menu-dropdown" style="display:none; position:absolute; right:0; top:36px; width:220px; background:var(--surface); border:1px solid var(--border); border-radius:10px; box-shadow:var(--shadow-md); padding:6px; z-index:2000;">
      <button class="mini-btn" id="theme-toggle" onclick="toggleTheme()" style="width:100%; text-align:left; padding:8px 10px; background:transparent; border:none; color:var(--text); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:8px;">
        <span id="theme-icon">🌙</span> <span id="theme-text">Modo Claro</span>
      </button>
      <button class="mini-btn" id="byok-btn" onclick="openAIConfigModal()" style="width:100%; text-align:left; padding:8px 10px; background:transparent; border:none; color:var(--text); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:8px;">
        🔑 <span>API Keys (BYOK)</span>
      </button>
      <button class="mini-btn" onclick="openAIConfigModalGuide()" style="width:100%; text-align:left; padding:8px 10px; background:transparent; border:none; color:var(--text); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:8px;">
        📖 <span>Guía de APIs</span>
      </button>
      <div style="height:1px; background:var(--border); margin:4px 0;"></div>
      <button class="mini-btn" onclick="exportVaultJson()" style="width:100%; text-align:left; padding:8px 10px; background:transparent; border:none; color:var(--text); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:8px;">
        💾 <span>Exportar Bóveda (.json)</span>
      </button>
      <button class="mini-btn" onclick="document.getElementById('vault-input').click()" style="width:100%; text-align:left; padding:8px 10px; background:transparent; border:none; color:var(--text); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:8px;">
        📥 <span>Restaurar Bóveda</span>
      </button>
      <input type="file" id="vault-input" accept=".json" onchange="importVaultJson(this.files[0])" style="display:none">
    </div>
  </div>
</header>"""

    html = header_old_pattern.sub(header_new, html)

    # 4. Add dropdown helper script
    dropdown_js = """
    function toggleMoreMenu(e) {
      if (e) e.stopPropagation();
      const menu = document.getElementById('more-menu-dropdown');
      if (menu) {
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
      }
    }
    document.addEventListener('click', function(e) {
      const menu = document.getElementById('more-menu-dropdown');
      const btn = document.getElementById('more-menu-btn');
      if (menu && btn && !menu.contains(e.target) && !btn.contains(e.target)) {
        menu.style.display = 'none';
      }
    });
    function closeConfigModal() {
      const menu = document.getElementById('more-menu-dropdown');
      if (menu) menu.style.display = 'none';
    }
    """
    if "toggleMoreMenu" not in html:
        html = html.replace("</script>\n</body>", dropdown_js + "\n</script>\n</body>")

    # 5. Update Sidebar task navigation
    sidebar_old_pattern = re.compile(r'<nav id="sidebar">.*?</nav>', re.DOTALL)
    sidebar_new = """<nav id="sidebar">
    <!-- TAREA 1: EXPLORAR -->
    <div class="nav-section" style="font-size:10px; letter-spacing:1px; color:var(--accent); font-weight:800; margin-top:6px;">EXPLORAR</div>
    <div class="nav-item active" data-section="network" onclick="navigate('network')">
      <span class="nav-icon">👥</span><span>Mi Red</span>
      <span class="nav-badge tabular-nums" id="nb-network">-</span>
    </div>
    <div class="nav-item" data-section="upload" onclick="navigate('upload')">
      <span class="nav-icon">📁</span><span>Cargar / Buscar Bóveda</span>
    </div>
    <div class="nav-item" data-section="messages" onclick="navigate('messages')">
      <span class="nav-icon">💬</span><span>Mensajes</span>
      <span class="nav-badge tabular-nums" id="nb-msgs">-</span>
    </div>

    <!-- TAREA 2: ENTENDER ICP & LEADS -->
    <div class="nav-section" style="font-size:10px; letter-spacing:1px; color:var(--purple); font-weight:800; margin-top:14px;">ENTENDER ICP & LEADS</div>
    <div class="nav-item" data-section="analytics" onclick="navigate('analytics')">
      <span class="nav-icon">📊</span><span>Analítica RevOps</span>
    </div>
    <div class="nav-item" data-section="icp" onclick="navigate('icp')">
      <span class="nav-icon">🎯</span><span>ICP / Leads</span>
      <span class="nav-badge tabular-nums" id="nb-icp">-</span>
    </div>
    <div class="nav-item" data-section="graph" onclick="navigate('graph')">
      <span class="nav-icon">🕸️</span><span>Red de Grafos</span>
      <span class="nav-badge" style="background:var(--purple); color:#fff;">COSMA</span>
    </div>
    <div class="nav-item" data-section="benchmarks" onclick="navigate('benchmarks')">
      <span class="nav-icon">📈</span><span>Benchmarks</span>
    </div>

    <!-- TAREA 3: GESTIONAR PIPELINE -->
    <div class="nav-section" style="font-size:10px; letter-spacing:1px; color:var(--green); font-weight:800; margin-top:14px;">GESTIONAR PIPELINE</div>
    <div class="nav-item" data-section="crm" onclick="navigate('crm')">
      <span class="nav-icon">💼</span><span>Mi Pipeline</span>
      <span class="nav-badge tabular-nums" id="nb-crm">0</span>
    </div>
    <div class="nav-item" data-section="purge" onclick="navigate('purge')">
      <span class="nav-icon">🧹</span><span>Depurar Bóveda & Limpieza</span>
      <span class="nav-badge tabular-nums" id="nb-purge">-</span>
    </div>
    <div class="nav-item" data-section="profile" onclick="navigate('profile')">
      <span class="nav-icon">👤</span><span>Mi Perfil</span>
    </div>
  </nav>"""

    html = sidebar_old_pattern.sub(sidebar_new, html)

    # 6. Integrate RadarCore in executeHeroTalkSearch
    old_talk_search = """function executeHeroTalkSearch() {"""
    new_talk_search = """function executeHeroTalkSearch() {
  const input = document.getElementById('network-talk-search');
  if (!input) return;
  const rawQuery = input.value.trim();
  if (!rawQuery) return;

  if (window.RadarCore && typeof window.RadarCore.searchVault === 'function') {
    const vault = { contacts: S.contacts || [], messages: S.messages || [] };
    const res = window.RadarCore.searchVault(vault, rawQuery);
    filteredContacts = res.contacts;
    if (S.loadedParts && !S.loadedParts.connections) S.loadedParts.connections = true;
    navigate('network');
    const searchInput = document.getElementById('net-search') || document.getElementById('search-input');
    if (searchInput) searchInput.value = rawQuery;
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    showToast(`📡 RadarCore: ${res.totalResults} resultados para "${rawQuery}" (${res.queryParsed.expandedTerms.slice(0,3).join(', ')}).`, '🔍');
    return;
  }
"""
    if old_talk_search in html and "RadarCore.searchVault" not in html:
        html = html.replace(old_talk_search, new_talk_search)

    with open(STAGING_PATH, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html)

    print("STAGING_PATCHED_SUCCESSFULLY")

if __name__ == "__main__":
    patch_staging()
