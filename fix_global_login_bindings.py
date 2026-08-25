import re

def fix_global_logins(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean top script bindings
    top_binding = "window.submitCustomLogin = submitCustomLogin;\nwindow.quickLogin = quickLogin;\nwindow.closeLoginModal = closeLoginModal;\n"
    
    if 'window.submitCustomLogin = submitCustomLogin;' not in content:
        content = content.replace("<script>", "<script>\n" + top_binding, 1)

    # 2. Add window assignment right inside submitCustomLogin function body
    old_func_hdr = "function submitCustomLogin(targetUser) {"
    new_func_hdr = """function submitCustomLogin(targetUser) {
  window.submitCustomLogin = submitCustomLogin;"""

    content = content.replace(old_func_hdr, new_func_hdr)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_global_logins(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_global_logins(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Global login function bindings updated!")
