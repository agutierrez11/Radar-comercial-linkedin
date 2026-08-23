import re

def fix_vault_a_dom_ids(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace map container ID
    content = content.replace(
        '<div id="gis-map" style="width:100%; height:320px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1;"></div>',
        '<div id="gis-map-container" style="width:100%; height:320px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1;"></div>'
    )

    # Replace filter bar inputs to match applyNetworkFilters IDs:
    # 'search-input' -> 'net-search'
    # 'filter-hier' -> 'net-hier'
    # 'filter-country' -> 'net-country'
    # 'contacts-tbody' -> 'net-tbody'
    
    old_filter_bar = """        <div class="filter-bar">
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
        </div>"""

    new_filter_bar = """        <div class="filter-bar">
          <div class="filter-group" style="flex:2">
            <label>Buscar en la red</label>
            <input class="filter-input" id="net-search" type="text" placeholder="Nombre, cargo, empresa, país, ciudad..." oninput="applyNetworkFilters()">
          </div>
          <div class="filter-group">
            <label>Jerarquía</label>
            <select class="filter-input" id="net-hier" onchange="applyNetworkFilters()">
              <option value="">Todas</option>
              <option value="C-Level">C-Level (CEO, CTO...)</option>
              <option value="Director">Director / VP</option>
              <option value="Gerente">Gerente / Manager</option>
              <option value="Otro">Otros cargos</option>
            </select>
          </div>
          <div class="filter-group">
            <label>País</label>
            <select class="filter-input" id="net-country" onchange="applyNetworkFilters()">
              <option value="">Todos los países</option>
            </select>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-size:12px; color:var(--text-muted);">
          <div id="net-counter">Mostrando contactos de tu red</div>
          <div style="display:flex; gap:8px; align-items:center;">
            <span>Orden:</span>
            <select class="filter-input" id="net-sort" onchange="applyNetworkFilters()" style="font-size:11px; padding:3px 8px;">
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
            <tbody id="net-tbody"></tbody>
          </table>
          <div id="net-empty" style="display:none; text-align:center; padding:30px; color:var(--text-muted);">
            No se encontraron contactos con los filtros seleccionados.
          </div>
        </div>"""

    if old_filter_bar in content:
        content = content.replace(old_filter_bar, new_filter_bar)
    else:
        # try regex replacement for table body and inputs
        content = content.replace('id="search-input"', 'id="net-search" oninput="applyNetworkFilters()"')
        content = content.replace('id="filter-hier"', 'id="net-hier" onchange="applyNetworkFilters()"')
        content = content.replace('id="filter-country"', 'id="net-country" onchange="applyNetworkFilters()"')
        content = content.replace('id="contacts-tbody"', 'id="net-tbody"')

    # In switchVaultViewMode, ensure invalidateSize is called on gisMapInstance when mode is A (emilkowalski-motion Rule 13)
    old_switch = "if (containerA) containerA.style.display = 'block';"
    new_switch = """if (containerA) containerA.style.display = 'block';
    if (typeof renderNetwork === 'function') renderNetwork();
    setTimeout(() => {
      if (typeof gisMapInstance !== 'undefined' && gisMapInstance && typeof gisMapInstance.invalidateSize === 'function') {
        gisMapInstance.invalidateSize();
      }
    }, 150);"""

    if old_switch in content and "invalidateSize" not in content[content.find("function switchVaultViewMode"):content.find("function switchVaultViewMode")+500]:
        content = content.replace(old_switch, new_switch, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_vault_a_dom_ids("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
fix_vault_a_dom_ids("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Fixed DOM IDs for GIS Map (gis-map-container) and classic table (net-tbody) in index.html and staging.html!")
