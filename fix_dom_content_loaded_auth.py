import re

def fix_dom_auth(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Guard DOMContentLoaded auto-restore
    old_dom = "document.addEventListener('DOMContentLoaded', async () => {\n  // 1. Intentar auto-restaurar"
    new_dom = """document.addEventListener('DOMContentLoaded', async () => {
  if (window.currentAuthUser && !window.currentAuthUser.isMaster) {
    console.log('[AutoVault Bootstrap] Skipped: Active user is isolated non-master.');
    return;
  }
  // 1. Intentar auto-restaurar"""

    content = content.replace(old_dom, new_dom)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_dom_auth(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_dom_auth(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("DOMContentLoaded auth guard applied!")
