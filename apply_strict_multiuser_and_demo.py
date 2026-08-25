import re

def patch_strict_auth_and_demo(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add critical CSS so login modal is display flex BY DEFAULT and main content is hidden until login
    critical_css = """
/* CRITICAL MULTI-TENANT AUTH GATING CSS */
#login-modal {
  display: flex !important;
  z-index: 99999 !important;
  position: fixed !important;
  top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(12px) !important;
}
#login-modal.closed {
  display: none !important;
}
body.not-authenticated #main-content,
body.not-authenticated .sidebar,
body.not-authenticated header {
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
"""

    if '/* CRITICAL MULTI-TENANT AUTH GATING CSS */' not in content:
        content = content.replace('</style>', critical_css + '\n</style>', 1)

    # Make sure body has 'not-authenticated' class initially
    content = content.replace('<body>', '<body class="not-authenticated">', 1)

    # 2. Update closeLoginModal and submitCustomLogin
    old_close_modal = "function closeLoginModal() {\n  const modal = document.getElementById('login-modal');\n  if (modal) modal.style.display = 'none';\n}"
    new_close_modal = """function closeLoginModal() {
  const modal = document.getElementById('login-modal');
  if (modal) modal.classList.add('closed');
  document.body.classList.remove('not-authenticated');
}"""
    content = content.replace(old_close_modal, new_close_modal)

    # Update submitCustomLogin to hide admin vault dropdown for non-admin users
    old_submit_login = "function submitCustomLogin(targetUser) {"
    new_submit_login = """function submitCustomLogin(targetUser) {
  const usernameInput = document.getElementById('login-username-input');
  const inputVal = usernameInput ? usernameInput.value : '';
  const username = (targetUser || inputVal || '').trim().toLowerCase();
  if (!username) return;

  closeLoginModal();
  const activeUserPill = document.getElementById('active-user-name');
  const activePillContainer = document.getElementById('active-user-pill');
  const adminDropdown = document.getElementById('admin-vault-dropdown');
  const ronanBanner = document.getElementById('ronan-ab-banner');

  if (username === 'antonio' || username === 'master') {
    window.currentAuthUser = { id: 'antonio', name: 'Antonio (Master)', isMaster: true };
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';
    if (activePillContainer) activePillContainer.style.cursor = 'pointer';
    if (ronanBanner) ronanBanner.style.display = 'none';
    restoreLocalVault().then(restored => {
      if (!restored) loadDemoData(false);
      updateStatus();
      if (typeof renderDashboard === 'function') renderDashboard();
      if (typeof renderNetworkTable === 'function') renderNetworkTable();
      showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
    });
  } else if (username === 'giovanna' || username === 'roanna') {
    const isGio = username === 'giovanna';
    const nameStr = isGio ? 'Giovanna' : 'Roanna';
    window.currentAuthUser = { id: username, name: `Bóveda Privada ${nameStr}`, isMaster: false };
    if (activeUserPill) activeUserPill.textContent = `🔒 Bóveda ${nameStr} (Privada)`;
    if (activePillContainer) { activePillContainer.style.cursor = 'default'; activePillContainer.onclick = null; }
    if (adminDropdown) adminDropdown.style.display = 'none';
    if (ronanBanner) ronanBanner.style.display = 'none';
    
    // Complete isolation: Vault is 100% EMPTY for non-master users!
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    S.crmState = { discarded: [], whitelisted: [], deals: [] };
    S.loadedParts = { connections: false, messages: false, positions: false, profile: false };
    S.isDemoLoaded = false;
    
    updateStatus();
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    navigate('upload');
    showToast(`🔒 Bóveda Aislada de ${nameStr} (0 contactos). Lista para cargar tu ZIP.`, '🔒');
  } else if (username === 'ronan') {
    window.currentAuthUser = { id: 'ronan', name: 'Sandbox Demo Ronan', isMaster: false, isSandbox: true };
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';
    if (activePillContainer) { activePillContainer.style.cursor = 'default'; activePillContainer.onclick = null; }
    if (adminDropdown) adminDropdown.style.display = 'none';
    if (ronanBanner) ronanBanner.style.display = 'flex';
    
    switchRonanAbMode('B');
  } else {
    // Custom user login
    window.currentAuthUser = { id: username, name: `Bóveda ${username}`, isMaster: false };
    if (activeUserPill) activeUserPill.textContent = `👤 Bóveda ${username}`;
    if (activePillContainer) { activePillContainer.style.cursor = 'default'; activePillContainer.onclick = null; }
    if (adminDropdown) adminDropdown.style.display = 'none';
    if (ronanBanner) ronanBanner.style.display = 'none';
    
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    updateStatus();
    navigate('upload');
    showToast(`🔒 Bóveda de ${username} lista.`, '🔑');
  }
}"""
    
    pattern_submit = r'function submitCustomLogin\(targetUser\)\s*\{[\s\S]*?\n\}'
    content = re.sub(pattern_submit, new_submit_login, content)

    # 3. Add Live Demo Control Bar in sec-upload
    demo_control_html = """
      <!-- ── LIVE DEMO & VAULT RESET CONTROL BAR ── -->
      <div style="margin-bottom:20px; padding:16px 20px; background:var(--surface); border:1px solid var(--border); border-radius:14px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; box-shadow:var(--shadow-sm);">
        <div>
          <div style="font-weight:700; font-size:13px; color:var(--text); display:flex; align-items:center; gap:8px;">
            <span>🎬 Control de Demo en Vivo & Reseteo</span>
            <span style="font-size:10px; background:rgba(79,70,229,0.15); color:var(--accent); padding:2px 8px; border-radius:12px; font-weight:700;">Zero-Knowledge</span>
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">
            Limpia la bóveda para hacer presentaciones en vivo o restaura tus 2,953 contactos maestros con 1 clic.
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <button class="mini-btn" onclick="clearVaultForLiveDemo()" style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); color:#ef4444; font-weight:700; font-size:11px; padding:7px 14px; border-radius:8px; cursor:pointer;">
            🧹 Vaciar Bóveda (Demo en Vivo)
          </button>
          <button class="mini-btn" onclick="loadDemoData(false)" style="background:var(--primary); color:#ffffff; font-weight:700; font-size:11px; padding:7px 14px; border-radius:8px; cursor:pointer;">
            ⚡ Restaurar Antonio Master (2,953)
          </button>
        </div>
      </div>
    """

    if '<!-- ── LIVE DEMO & VAULT RESET CONTROL BAR ── -->' not in content:
        content = content.replace('<div class="upload-container">', demo_control_html + '\n<div class="upload-container">', 1)

    # 4. Add clearVaultForLiveDemo JS function
    clear_func_js = """
function clearVaultForLiveDemo() {
  if (confirm("⚠️ ¿Vaciar completamente la bóveda para hacer una Demo en Vivo?\\n\\nPodrás arrastrar tu archivo ZIP o restaurar tus 2,953 contactos maestros en cualquier momento.")) {
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    S.crmState = { discarded: [], whitelisted: [], deals: [] };
    S.loadedParts = { connections: false, messages: false, positions: false, profile: false };
    S.isDemoLoaded = false;
    try { localStorage.clear(); } catch(e){}
    updateStatus();
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    navigate('upload');
    showToast('🧹 Bóveda vaciada para Demo en Vivo. Lista para arrastrar tu archivo.', 'ℹ️');
  }
}
window.clearVaultForLiveDemo = clearVaultForLiveDemo;
"""
    if 'function clearVaultForLiveDemo()' not in content:
        content = content.replace("function submitCustomLogin", clear_func_js + "\nfunction submitCustomLogin")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_strict_auth_and_demo(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_strict_auth_and_demo(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Strict auth gating and demo control bar applied!")
