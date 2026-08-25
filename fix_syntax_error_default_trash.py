import re

def fix_trash(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("}default'; activePillContainer.onclick = null; }", "if (activePillContainer) { activePillContainer.style.cursor = 'default'; activePillContainer.onclick = null; }")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_trash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_trash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Syntax error default trash string removed!")
