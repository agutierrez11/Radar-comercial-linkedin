import re

def update_multitenant_security(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Protect quickLogin for Antonio with Admin PIN check if requested from public gateway
    old_quick_login = """function quickLogin(username, pwd) {
  const usernameInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  if (usernameInput) usernameInput.value = username;
  if (pwdInput) pwdInput.value = pwd;
  submitCustomLogin(username);
}"""

    new_quick_login = """function quickLogin(username, pwd) {
  const usernameInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');

  if (username === 'antonio' || username === 'master') {
    const adminPin = prompt('🔒 Bóveda Privada del Administrador (Antonio).\\nIngresa el PIN de Administrador (ej. 12345):');
    if (!adminPin || adminPin.trim() !== '12345') {
      showToast('❌ PIN de Administrador incorrecto. Acceso denegado.', '🔒');
      return;
    }
  }

  if (usernameInput) usernameInput.value = username;
  if (pwdInput) pwdInput.value = pwd;
  submitCustomLogin(username);
}"""

    if old_quick_login in content:
        content = content.replace(old_quick_login, new_quick_login)

    # 2. Update submitCustomLogin to handle Admin Auth & Multi-Tenant isolation
    old_submit_login_start = "if (username === 'antonio' || username === 'master') {"
    new_submit_login_start = """if (username === 'antonio' || username === 'master') {
    const pwdInput = document.getElementById('login-password-input');
    const pwdVal = pwdInput ? pwdInput.value : '';
    if (pwdVal && pwdVal !== '12345' && pwdVal !== 'admin') {
      showToast('❌ Contraseña de Administrador incorrecta.', '🔒');
      return;
    }"""

    if old_submit_login_start in content and 'Contraseña de Administrador incorrecta' not in content:
        content = content.replace(old_submit_login_start, new_submit_login_start, 1)

    # 3. Add explicit Admin Vault Switcher dropdown menu on active-user-pill
    old_pill = """<div class="kpi-pill" id="active-user-pill" onclick="openLoginModal()" style="cursor:pointer !important; background:rgba(79,70,229,0.12); border:1px solid var(--accent); color:var(--text); font-weight:700; font-size:11px; padding:4px 10px; border-radius:20px; display:flex; align-items:center; gap:6px;" title="Cambiar usuario/bóveda">
    <span class="dot" style="width:7px; height:7px; border-radius:50%; background:var(--green); display:inline-block;"></span>
    <span id="active-user-name">👤 Antonio</span>
  </div>"""

    new_pill = """<div class="dropdown-container" style="position:relative;">
    <div class="kpi-pill" id="active-user-pill" onclick="toggleAdminVaultMenu(event)" style="cursor:pointer !important; background:rgba(79,70,229,0.12); border:1px solid var(--accent); color:var(--text); font-weight:700; font-size:11px; padding:4px 10px; border-radius:20px; display:flex; align-items:center; gap:6px;" title="Cambiar usuario/bóveda">
      <span class="dot" style="width:7px; height:7px; border-radius:50%; background:var(--green); display:inline-block;"></span>
      <span id="active-user-name">👤 Antonio (Master)</span> ▾
    </div>
    <div id="admin-vault-dropdown" style="display:none; position:absolute; right:0; top:32px; width:260px; background:var(--surface); border:1px solid var(--border); border-radius:12px; box-shadow:var(--shadow-md); padding:8px; z-index:2500; font-family:'Outfit',sans-serif;">
      <div style="font-size:10px; font-weight:800; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; padding:4px 8px; margin-bottom:4px;">👑 Conmutador Multi-Tenant (Admin)</div>
      <button class="mini-btn" onclick="submitCustomLogin('antonio'); toggleAdminVaultMenu();" style="width:100%; text-align:left; padding:8px 10px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2); color:var(--text); border-radius:8px; margin-bottom:4px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
        <span>👤 <strong>Antonio</strong> (Master)</span>
        <span style="font-size:9px; background:rgba(16,185,129,0.2); color:var(--green); padding:1px 6px; border-radius:4px; font-weight:700;">2,953 cont.</span>
      </button>
      <button class="mini-btn" onclick="submitCustomLogin('giovanna'); toggleAdminVaultMenu();" style="width:100%; text-align:left; padding:8px 10px; background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2); color:var(--purple); border-radius:8px; margin-bottom:4px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
        <span>🔒 <strong>Giovanna</strong> (Bóveda Privada)</span>
        <span style="font-size:9px; background:rgba(124,58,237,0.2); color:var(--purple); padding:1px 6px; border-radius:4px; font-weight:700;">Aislada</span>
      </button>
      <button class="mini-btn" onclick="submitCustomLogin('ronan'); toggleAdminVaultMenu();" style="width:100%; text-align:left; padding:8px 10px; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:var(--amber); border-radius:8px; margin-bottom:6px; font-size:11px; display:flex; justify-content:space-between; align-items:center;">
        <span>🧪 <strong>Ronan</strong> (Sandbox BI)</span>
        <span style="font-size:9px; background:rgba(245,158,11,0.2); color:var(--amber); padding:1px 6px; border-radius:4px; font-weight:700;">500 demo</span>
      </button>
      <div style="border-top:1px solid var(--border); padding-top:6px; display:flex; justify-content:space-between;">
        <button class="mini-btn" onclick="openLoginModal(); toggleAdminVaultMenu();" style="font-size:10px; color:var(--text-muted); background:transparent; border:none; padding:4px 6px; cursor:pointer;">🔑 Abrir Modal Login</button>
      </div>
    </div>
  </div>"""

    if old_pill in content:
        content = content.replace(old_pill, new_pill)

    # Add toggleAdminVaultMenu function in JS
    if 'function toggleAdminVaultMenu' not in content:
        toggle_func = """
function toggleAdminVaultMenu(e) {
  if (e) e.stopPropagation();
  const dropdown = document.getElementById('admin-vault-dropdown');
  if (dropdown) {
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
  }
}
window.toggleAdminVaultMenu = toggleAdminVaultMenu;
document.addEventListener('click', () => {
  const dropdown = document.getElementById('admin-vault-dropdown');
  if (dropdown) dropdown.style.display = 'none';
});
"""
        content = content.replace("window.submitCustomLogin = submitCustomLogin;", "window.submitCustomLogin = submitCustomLogin;\n" + toggle_func)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_multitenant_security("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\index.html")
update_multitenant_security("c:\\Users\\Antonio\\.gemini\\antigravity-ide\\scratch\\radar-comercial\\staging.html")
print("✅ Updated Multi-Tenant Security & Admin PIN protection in index.html and staging.html!")
