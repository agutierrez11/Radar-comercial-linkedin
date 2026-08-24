import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove duplicate <div class="section" id="sec-network"> block (lines 1263-1360 approx)
    # Search for second occurrence of id="sec-network"
    first_net_idx = content.find('id="sec-network"')
    if first_net_idx != -1:
        second_net_idx = content.find('id="sec-network"', first_net_idx + 20)
        if second_net_idx != -1:
            # Find the end of the second sec-network block (before id="sec-icp")
            icp_idx = content.find('id="sec-icp"', second_net_idx)
            if icp_idx != -1:
                # Find start of <div class="section" before second_net_idx
                sec_start = content.rfind('<div class="section"', first_net_idx + 20, second_net_idx + 10)
                if sec_start != -1:
                    content = content[:sec_start] + content[icp_idx - 25:]

    # 2. Remove duplicate sec-analytics header if present
    # Check for duplicate sec-analytics
    first_ana_idx = content.find('id="sec-analytics"')
    if first_ana_idx != -1:
        second_ana_idx = content.find('id="sec-analytics"', first_ana_idx + 20)
        if second_ana_idx != -1:
            bench_idx = content.find('id="sec-benchmarks"', second_ana_idx)
            if bench_idx != -1:
                sec_start = content.rfind('<div class="section"', first_ana_idx + 20, second_ana_idx + 10)
                if sec_start != -1:
                    content = content[:sec_start] + content[bench_idx - 25:]

    # 3. Restore Map Tile Switcher Buttons in map-gis-card
    old_map_header = """<div style="display:flex; align-items:center; gap:8px;">
              <button class="mini-btn" onclick="resetMapZoom()" style="padding:4px 8px; font-size:11px;">🔍 Re-centrar Mapa</button>
            </div>"""

    new_map_header = """<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <button class="mini-btn" onclick="switchGisTileLayer('dark')" style="padding:4px 8px; font-size:10px; font-weight:700;">🌙 Oscuro</button>
              <button class="mini-btn" onclick="switchGisTileLayer('light')" style="padding:4px 8px; font-size:10px; font-weight:700;">☀️ Claro</button>
              <button class="mini-btn" onclick="switchGisTileLayer('satellite')" style="padding:4px 8px; font-size:10px; font-weight:700;">🛰️ Satélite</button>
              <button class="mini-btn" onclick="resetMapZoom()" style="padding:4px 8px; font-size:11px; font-weight:700; background:var(--accent); color:#fff;">🔍 Re-centrar Mapa</button>
            </div>"""

    if old_map_header in content:
        content = content.replace(old_map_header, new_map_header)

    # 4. Fix sec-analytics unlocking: ensure renderAnalytics() hides locked state and shows dashboard!
    unlock_analytics_func = """
function unlockAnalyticsUI() {
  const locked = document.getElementById('analytics-locked');
  const dash = document.getElementById('analytics-dashboard');
  if (locked) locked.style.display = 'none';
  if (dash) dash.style.display = 'block';
  if (typeof renderAnalytics === 'function') renderAnalytics();
  if (typeof renderPowerBiEcharts === 'function' && window.currentAnalyticsViewMode === 'B') renderPowerBiEcharts();
}
window.unlockAnalyticsUI = unlockAnalyticsUI;
"""

    if 'function unlockAnalyticsUI' not in content:
        content = content.replace("window.submitCustomLogin = submitCustomLogin;", "window.submitCustomLogin = submitCustomLogin;\n" + unlock_analytics_func)

    # Ensure submitCustomLogin calls unlockAnalyticsUI()
    if 'unlockAnalyticsUI();' not in content:
        content = content.replace("renderNetworkTable();", "renderNetworkTable();\n    unlockAnalyticsUI();")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_file("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
clean_file("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Cleaned duplicate sections and restored map tile controls & analytics unlocking in index.html and staging.html!")
