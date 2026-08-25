import re

def fix_render_dash(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update closeLoginModal to remove body class
    old_close = """function closeLoginModal() {
  console.log('[LoginModal] Closing login modal...');
  const modal = document.getElementById('login-modal');
  if (modal) {
    modal.classList.remove('open');
    modal.style.setProperty('display', 'none', 'important');
    modal.style.setProperty('opacity', '0', 'important');
    modal.style.setProperty('pointer-events', 'none', 'important');
  }
}"""

    new_close = """function closeLoginModal() {
  console.log('[LoginModal] Closing login modal...');
  const modal = document.getElementById('login-modal');
  if (modal) {
    modal.classList.remove('open');
    modal.style.setProperty('display', 'none', 'important');
    modal.style.setProperty('opacity', '0', 'important');
    modal.style.setProperty('pointer-events', 'none', 'important');
  }
  document.body.classList.remove('not-authenticated');
}"""

    content = content.replace(old_close, new_close)

    # 2. Update renderDashboard to respect window.currentAuthUser.name
    old_dash = "const activeUserPill = document.getElementById('active-user-name');"
    new_dash = """const activeUserPill = document.getElementById('active-user-name');
  if (activeUserPill && window.currentAuthUser) {
    activeUserPill.textContent = window.currentAuthUser.name;
  }"""

    content = content.replace(old_dash, new_dash)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_render_dash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_render_dash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Render dashboard user name fix applied!")
