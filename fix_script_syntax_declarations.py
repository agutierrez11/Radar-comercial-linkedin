import re

def fix_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace 'let gisMap' and 'let gisMapInstance' and 'let cosma' with 'var'
    content = content.replace("let gisMap;", "var gisMap;")
    content = content.replace("let gisMapInstance;", "var gisMapInstance;")
    content = content.replace("let gisLayerGroup;", "var gisLayerGroup;")
    content = content.replace("let gisMapMarkers = [];", "var gisMapMarkers = [];")
    content = content.replace("let cosmaGraphNodes;", "var cosmaGraphNodes;")
    content = content.replace("let cosmaGraphLinks;", "var cosmaGraphLinks;")
    content = content.replace("let analyticsChartInstance;", "var analyticsChartInstance;")

    # Remove the top global block if it has duplicate declarations
    content = re.sub(r'<script>\s*// GLOBAL VAR DECLARATIONS[\s\S]*?</script>', '', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_script(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_script(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
