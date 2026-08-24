import re

def fix_map(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Define global resetMapZoom function if missing or incomplete
    reset_map_js = """
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

    if 'function resetMapZoom' not in content:
        content = content.replace("window.submitCustomLogin = submitCustomLogin;", "window.submitCustomLogin = submitCustomLogin;\n" + reset_map_js)

    # 2. Fix map container CSS styling to ensure 100% width and full responsiveness
    content = content.replace(
        'id="gis-map-container" style="width:100%; height:320px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1;"',
        'id="gis-map-container" style="width:100% !important; min-width:100%; height:340px; border-radius:10px; border:1px solid var(--border); background:var(--bg); z-index:1; overflow:hidden;"'
    )

    # 3. Ensure renderGISMap calls invalidateSize properly on window resize & render
    if 'window.addEventListener(\'resize\', () => { if (gisMapInstance) gisMapInstance.invalidateSize(); });' not in content:
        content = content.replace(
            "gisMapInstance.invalidateSize();\n  }, 250);",
            "gisMapInstance.invalidateSize();\n  }, 250);\n  window.addEventListener('resize', () => { if (gisMapInstance) gisMapInstance.invalidateSize(); });"
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_map("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
fix_map("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Fixed resetMapZoom and 100% width map container in index.html and staging.html!")
