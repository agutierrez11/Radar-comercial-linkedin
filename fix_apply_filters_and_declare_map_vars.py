import re

def fix_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace unsafe applyNetworkFilters lines 3784-3787
    old_code = """  const search = norm(document.getElementById('net-search').value);
  const country = document.getElementById('net-country').value;
  const hier = document.getElementById('net-hier').value;
  const sector = document.getElementById('net-sector').value;"""

    new_code = """  const netSearchEl = document.getElementById('net-search') || document.getElementById('network-talk-search');
  const countryEl = document.getElementById('net-country');
  const hierEl = document.getElementById('net-hier');
  const sectorEl = document.getElementById('net-sector');

  const search = netSearchEl ? norm(netSearchEl.value) : '';
  const country = countryEl ? countryEl.value : '';
  const hier = hierEl ? hierEl.value : '';
  const sector = sectorEl ? sectorEl.value : '';"""

    if old_code in content:
        content = content.replace(old_code, new_code)

    # 2. Inject global var declarations for GIS map and Cosma graph
    global_vars = """
<script>
var gisMapInstance = null;
var gisMap = null;
var gisLayerGroup = null;
var gisMapMarkers = [];
var cosmaGraphNodes = [];
var cosmaGraphLinks = [];
var analyticsChartInstance = null;

window.gisMapInstance = gisMapInstance;
window.gisMap = gisMap;
window.cosmaGraphNodes = cosmaGraphNodes;
</script>
"""

    if 'var gisMapInstance = null;' not in content:
        content = content.replace("<body>", "<body>\n" + global_vars)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
