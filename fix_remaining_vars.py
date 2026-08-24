import re

def fix_remaining(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Declare filterVerifiedOnly and cosmaSelectedNodeId at top with var
    top_vars = """
<script>
var filterVerifiedOnly = false;
var cosmaSelectedNodeId = null;
var cosmaGraphNodes = [];
var cosmaGraphLinks = [];
var gisMapInstance = null;
var gisMap = null;
var gisLayerGroup = null;
var gisMapMarkers = [];
var analyticsChartInstance = null;
</script>
"""

    content = content.replace("let filterVerifiedOnly = false;", "filterVerifiedOnly = false;")
    content = content.replace("let cosmaSelectedNodeId = null;", "cosmaSelectedNodeId = null;")

    if 'var filterVerifiedOnly' not in content:
        content = content.replace("<body>", "<body>\n" + top_vars)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_remaining(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_remaining(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
