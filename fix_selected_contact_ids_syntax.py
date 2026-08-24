import re

def fix_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change all let selectedContactIds to var selectedContactIds
    content = content.replace("let selectedContactIds = new Set();", "selectedContactIds = window.selectedContactIds || new Set();")
    content = content.replace("let selectedContactIds = ", "var selectedContactIds = ")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
