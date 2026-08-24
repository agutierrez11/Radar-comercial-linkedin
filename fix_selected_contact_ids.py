import re

def fix_selected(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Declare var selectedContactIds at top script block
    top_vars = "var selectedContactIds = window.selectedContactIds || new Set();\nwindow.selectedContactIds = selectedContactIds;"
    content = content.replace("let selectedContactIds = new Set();", "selectedContactIds = window.selectedContactIds || new Set();")

    if 'var selectedContactIds' not in content:
        content = content.replace("<body>", "<body>\n<script>" + top_vars + "</script>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_selected(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_selected(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
