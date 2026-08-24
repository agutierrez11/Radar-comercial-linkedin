import re

def fix_all_inits(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject var declarations at top of script to prevent 'Cannot access X before initialization'
    top_vars = """
<script>
// GLOBAL VAR DECLARATIONS (Prevent Temporal Dead Zone Errors)
var gisMapInstance = window.gisMapInstance || null;
var gisMap = window.gisMap || null;
var gisLayerGroup = window.gisLayerGroup || null;
var gisMapMarkers = window.gisMapMarkers || [];
var cosmaGraphNodes = window.cosmaGraphNodes || [];
var cosmaGraphLinks = window.cosmaGraphLinks || [];
var analyticsChartInstance = window.analyticsChartInstance || null;

window.gisMapInstance = gisMapInstance;
window.gisMap = gisMap;
window.cosmaGraphNodes = cosmaGraphNodes;
</script>
"""

    if 'var gisMapInstance' not in content:
        content = content.replace("<body>", "<body>\n" + top_vars)

    # 2. Fix applyNetworkFilters null checks for net-search, net-hier, net-country, net-sort
    old_apply_filters = """function applyNetworkFilters() {"""
    new_apply_filters = """function applyNetworkFilters() {
  const searchInput = document.getElementById('net-search') || document.getElementById('network-talk-search');
  const hierInput = document.getElementById('net-hier');
  const countryInput = document.getElementById('net-country');
  const sortInput = document.getElementById('net-sort');

  const q = searchInput ? (searchInput.value || '').toLowerCase().trim() : '';
  const h = hierInput ? hierInput.value : '';
  const c = countryInput ? countryInput.value : '';
  const s = sortInput ? sortInput.value : 'name-asc';"""

    if old_apply_filters in content:
        content = content.replace(old_apply_filters, new_apply_filters)

    # Replace usages of direct getElementById inside applyNetworkFilters if any
    content = content.replace(
        "const query = document.getElementById('net-search').value.toLowerCase();",
        "// safe query used above"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_all_inits(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_all_inits(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
