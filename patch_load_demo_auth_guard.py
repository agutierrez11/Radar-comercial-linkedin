import re

def patch_auth_guard(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Guard loadDemoData against non-master users
    old_load = "async function loadDemoData(autoNavigate = true) {\n  setLoading(true, 50);"
    new_load = """async function loadDemoData(autoNavigate = true) {
  if (window.currentAuthUser && !window.currentAuthUser.isMaster) {
    console.log('[LoadDemo] Aborted: Current auth user is isolated non-master.');
    return;
  }
  setLoading(true, 50);"""

    content = content.replace(old_load, new_load)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_auth_guard(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_auth_guard(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Load demo auth guard applied!")
