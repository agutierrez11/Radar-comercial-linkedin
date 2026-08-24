import re

def fix_const(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("const selectedContactIds = new Set();", "selectedContactIds = window.selectedContactIds || new Set();")
    content = content.replace("var selectedContactIds = window.selectedContactIds || new Set();\nwindow.selectedContactIds = selectedContactIds;", "")

    # Clean top script tag if empty
    content = content.replace("<script></script>", "")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_const(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_const(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
