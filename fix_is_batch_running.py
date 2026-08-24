import re

def fix_batch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("let isBatchRunning = false;", "isBatchRunning = false;")
    if 'var isBatchRunning = false;' not in content:
        content = content.replace("<script>", "<script>\nvar isBatchRunning = false;\nwindow.isBatchRunning = isBatchRunning;", 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_batch(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_batch(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
