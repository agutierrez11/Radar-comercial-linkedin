import re

def fix_globals(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    global_funcs = """
<script>
// 🗺️ RE-CENTRAR MAPA Y AUTO-FIT (emilkowalski-motion Rule 13)
function resetMapZoom() {
  try {
    const targetMap = window.gisMapInstance || window.gisMap;
    if (targetMap && typeof targetMap.setView === 'function') {
      targetMap.setView([15.0, -70.0], 3);
      if (typeof targetMap.invalidateSize === 'function') targetMap.invalidateSize();
      if (typeof showToast === 'function') showToast('🗺️ Mapa re-centrado a vista global.', '🗺️');
    }
  } catch (err) {
    console.warn('Map recenter error:', err);
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

// 📈 UNLOCK ANALYTICS UI
function unlockAnalyticsUI() {
  const locked = document.getElementById('analytics-locked');
  const dash = document.getElementById('analytics-dashboard');
  if (locked) locked.style.display = 'none';
  if (dash) dash.style.display = 'block';
  if (typeof renderAnalytics === 'function') renderAnalytics();
  if (typeof renderPowerBiEcharts === 'function' && window.currentAnalyticsViewMode === 'B') renderPowerBiEcharts();
}
window.unlockAnalyticsUI = unlockAnalyticsUI;
</script>
"""

    # Replace old head script block
    content = re.sub(r'<script>\s*// 🗺️ RE-CENTRAR MAPA[\s\S]*?</script>', global_funcs, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_globals(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_globals(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
