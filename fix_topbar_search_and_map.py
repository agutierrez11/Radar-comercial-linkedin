import re

def patch_topbar_and_map(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update #network-talk-search input to trigger oninput as well as onkeyup
    content = content.replace(
        'onkeyup="handleTalkToNetworkSearch(event)"',
        'oninput="handleTalkToNetworkSearch(event)" onkeyup="handleTalkToNetworkSearch(event)"'
    )

    # 2. Add handleTalkToNetworkSearch & resetMapZoom JS functions
    js_fixes = """
// 🔍 BÚSQUEDA HÉROE DESDE LA BARRA SUPERIOR (TOPBAR SEARCH)
function handleTalkToNetworkSearch(e) {
  const input = document.getElementById('network-talk-search');
  if (!input) return;
  const q = (input.value || '').trim();

  // Cambiar automáticamente a la vista de red si estamos en otra pestaña
  if (window.currentActiveSection !== 'network' && typeof navigate === 'function') {
    navigate('network');
  }

  // Sincronizar con el input de búsqueda de la Vista A
  const netSearch = document.getElementById('net-search');
  if (netSearch) {
    netSearch.value = q;
  }

  # Sincronizar con el input de búsqueda de la Vista B
  const bSearch = document.getElementById('vault-b-search-input');
  if (bSearch) {
    bSearch.value = q;
  }

  // Aplicar filtros en la red local
  if (typeof applyNetworkFilters === 'function') {
    applyNetworkFilters();
  }

  if (typeof renderVaultBFeed === 'function' && window.currentVaultViewMode === 'B') {
    renderVaultBFeed();
  }
}
window.handleTalkToNetworkSearch = handleTalkToNetworkSearch;

// 🗺️ RE-CENTRAR MAPA Y AUTO-FIT (emilkowalski-motion Rule 13)
function resetMapZoom() {
  if (typeof gisMapInstance !== 'undefined' && gisMapInstance) {
    gisMapInstance.setView([15.0, -70.0], 3);
    gisMapInstance.invalidateSize();
    if (typeof showToast === 'function') showToast('🗺️ Mapa re-centrado a vista global.', '🗺️');
  } else if (typeof gisMap !== 'undefined' && gisMap) {
    gisMap.setView([20, -10], 2);
    gisMap.invalidateSize();
    if (typeof showToast === 'function') showToast('🗺️ Mapa re-centrado a vista global.', '🗺️');
  }
}
window.resetMapZoom = resetMapZoom;
"""

    if 'function handleTalkToNetworkSearch' not in content:
        content = content.replace("window.submitCustomLogin = submitCustomLogin;", "window.submitCustomLogin = submitCustomLogin;\n" + js_fixes)

    # 3. Ensure map container uses 100% width and no truncation
    content = content.replace(
        'id="gis-map-container" style="width:100%; height:320px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1;"',
        'id="gis-map-container" style="width:100% !important; min-width:100%; height:340px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1; overflow:hidden;"'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_topbar_and_map("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
patch_topbar_and_map("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Fixed handleTalkToNetworkSearch and resetMapZoom in index.html and staging.html!")
