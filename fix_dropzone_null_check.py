import re

def fix_drop(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_drop = """const dropZone = document.getElementById('drop-zone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {"""

    new_drop = """const dropZone = document.getElementById('drop-zone');
if (dropZone) {
  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {"""

    if old_drop in content:
        content = content.replace(old_drop, new_drop)
        # Add closing brace
        content = content.replace("handleFiles(e.dataTransfer.files);\n});", "handleFiles(e.dataTransfer.files);\n});\n}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_drop(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_drop(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
