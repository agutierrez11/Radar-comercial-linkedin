import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace duplicate let declarations with simple assignments
    content = content.replace("let analyticsChartInstance = null;", "analyticsChartInstance = null;")
    content = content.replace("let cosmaGraphNodes = [];", "cosmaGraphNodes = [];")
    content = content.replace("let cosmaGraphNodes = null;", "cosmaGraphNodes = [];")
    content = content.replace("let cosmaGraphLinks = [];", "cosmaGraphLinks = [];")
    content = content.replace("let cosmaGraphLinks = null;", "cosmaGraphLinks = [];")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_file(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
