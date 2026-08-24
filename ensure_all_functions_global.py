import re

def fix_globals(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    global_funcs = """
<script>
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

// 🔍 BÚSQUEDA HÉROE DESDE LA BARRA SUPERIOR (TOPBAR SEARCH)
function handleTalkToNetworkSearch(e) {
  const input = document.getElementById('network-talk-search');
  if (!input) return;
  const q = (input.value || '').trim();

  if (window.currentActiveSection !== 'network' && typeof navigate === 'function') {
    navigate('network');
  }

  const netSearch = document.getElementById('net-search');
  if (netSearch) netSearch.value = q;

  const bSearch = document.getElementById('vault-b-search-input');
  if (bSearch) bSearch.value = q;

  if (typeof applyNetworkFilters === 'function') applyNetworkFilters();
  if (typeof renderVaultBFeed === 'function' && window.currentVaultViewMode === 'B') renderVaultBFeed();
}
window.handleTalkToNetworkSearch = handleTalkToNetworkSearch;
</script>
"""

    if 'function resetMapZoom' not in content:
        # Inject right after <head> or at start of <body>
        content = content.replace("<body>", "<body>\n" + global_funcs)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_globals("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
fix_globals("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Injected global functions resetMapZoom and handleTalkToNetworkSearch into index.html and staging.html!")
