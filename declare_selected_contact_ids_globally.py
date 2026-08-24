import re

def fix_global_set(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Declare var selectedContactIds = new Set(); in top script block
    top_declaration = "var selectedContactIds = new Set();\nwindow.selectedContactIds = selectedContactIds;"

    if 'var selectedContactIds = new Set();' not in content:
        content = content.replace("<script>", "<script>\n" + top_declaration + "\n", 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_global_set(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_global_set(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
