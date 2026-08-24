import re

def apply_clean_qa_fixes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Global top-level variables at top of body
    global_vars_block = """<script>
window.filterVerifiedOnly = false;
window.cosmaSelectedNodeId = null;
window.cosmaGraphNodes = window.cosmaGraphNodes || [];
window.cosmaGraphLinks = window.cosmaGraphLinks || [];
window.gisMapInstance = window.gisMapInstance || null;
window.gisMap = window.gisMap || null;
window.gisLayerGroup = window.gisLayerGroup || null;
window.gisMapMarkers = window.gisMapMarkers || [];
window.analyticsChartInstance = window.analyticsChartInstance || null;
window.selectedContactIds = window.selectedContactIds || new Set();
window.isBatchRunning = false;
window.COUNTRY_COORDS = window.COUNTRY_COORDS || {};
window.CITY_COORDS = window.CITY_COORDS || {};
var filterVerifiedOnly = window.filterVerifiedOnly;
var cosmaSelectedNodeId = window.cosmaSelectedNodeId;
var cosmaGraphNodes = window.cosmaGraphNodes;
var cosmaGraphLinks = window.cosmaGraphLinks;
var gisMapInstance = window.gisMapInstance;
var gisMap = window.gisMap;
var gisLayerGroup = window.gisLayerGroup;
var gisMapMarkers = window.gisMapMarkers;
var analyticsChartInstance = window.analyticsChartInstance;
var selectedContactIds = window.selectedContactIds;
var isBatchRunning = window.isBatchRunning;
var COUNTRY_COORDS = window.COUNTRY_COORDS;
var CITY_COORDS = window.CITY_COORDS;
</script>
"""

    if "window.filterVerifiedOnly = false;" not in content:
        content = content.replace("<body>", "<body>\n" + global_vars_block, 1)

    # 2. Replace redeclarations of let/const for these global variables
    content = content.replace("let filterVerifiedOnly = false;", "filterVerifiedOnly = false;")
    content = content.replace("let cosmaSelectedNodeId = null;", "cosmaSelectedNodeId = null;")
    content = content.replace("let cosmaGraphNodes = [];", "cosmaGraphNodes = [];")
    content = content.replace("let cosmaGraphNodes = null;", "cosmaGraphNodes = [];")
    content = content.replace("let cosmaGraphLinks = [];", "cosmaGraphLinks = [];")
    content = content.replace("let cosmaGraphLinks = null;", "cosmaGraphLinks = [];")
    content = content.replace("let gisMapInstance = null;", "gisMapInstance = null;")
    content = content.replace("let gisMap = null;", "gisMap = null;")
    content = content.replace("let gisLayerGroup = null;", "gisLayerGroup = null;")
    content = content.replace("let gisMapMarkers = [];", "gisMapMarkers = [];")
    content = content.replace("let analyticsChartInstance = null;", "analyticsChartInstance = null;")
    content = content.replace("let selectedContactIds = new Set();", "selectedContactIds = window.selectedContactIds || new Set();")
    content = content.replace("const selectedContactIds = new Set();", "selectedContactIds = window.selectedContactIds || new Set();")
    content = content.replace("let isBatchRunning = false;", "isBatchRunning = false;")
    content = content.replace("const COUNTRY_COORDS =", "COUNTRY_COORDS =")
    content = content.replace("const CITY_COORDS =", "CITY_COORDS =")

    # 3. Add null check to dropZone
    old_drop = "dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });"
    new_drop = "if (dropZone) { dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); }); }"
    if old_drop in content:
        content = content.replace(old_drop, new_drop)

    # 4. Safe populateFilters null checks
    content = content.replace(
        "const sel = document.getElementById('net-country');\n  sel.innerHTML =",
        "const sel = document.getElementById('net-country');\n  if (sel) sel.innerHTML ="
    )
    content = content.replace(
        "const sels = document.getElementById('net-sector');\n  sels.innerHTML =",
        "const sels = document.getElementById('net-sector');\n  if (sels) sels.innerHTML ="
    )

    # 5. Remove duplicate enrichSingleContactLive cleanly
    pattern = r'async function enrichSingleContactLive\(contactId\)\s*\{[\s\S]*?\n\}'
    matches = list(re.finditer(pattern, content))
    if len(matches) > 1:
        # keep first, remove second
        second_match = matches[1]
        content = content[:second_match.start()] + content[second_match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

apply_clean_qa_fixes(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
apply_clean_qa_fixes(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("QA fixes applied successfully!")
