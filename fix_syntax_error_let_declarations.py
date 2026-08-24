import re

def fix_redeclarations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change let gisMap = null; to var gisMap = null; or remove let
    content = content.replace("let gisMap = null;", "gisMap = null;")
    content = content.replace("let gisMapInstance = null;", "gisMapInstance = null;")
    content = content.replace("let gisLayerGroup = null;", "gisLayerGroup = null;")
    content = content.replace("let gisMapMarkers = [];", "gisMapMarkers = [];")
    content = content.replace("var gisMapMarkers = [];", "gisMapMarkers = [];")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_redeclarations(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_redeclarations(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
