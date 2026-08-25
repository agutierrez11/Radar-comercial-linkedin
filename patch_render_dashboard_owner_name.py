import re

def patch_render_dashboard(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update renderDashboard to check window.currentAuthUser
    old_code = "if (activeUserPill) activeUserPill.textContent = '👤 ' + (S.ownerName || 'Antonio (Master)');"
    new_code = """if (activeUserPill) {
    if (window.currentAuthUser && window.currentAuthUser.name) {
      activeUserPill.textContent = window.currentAuthUser.name;
    } else {
      activeUserPill.textContent = '👤 ' + (S.ownerName || 'Antonio (Master)');
    }
  }"""

    if old_code in content:
        content = content.replace(old_code, new_code)
    else:
        # Replace any direct textContent assignment in renderDashboard
        pattern = r"if \(activeUserPill\)\s*activeUserPill\.textContent\s*=\s*['\"`][^'\"]+['\"`]"
        content = re.sub(pattern, new_code, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_render_dashboard(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_render_dashboard(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Render dashboard owner name patch applied!")
