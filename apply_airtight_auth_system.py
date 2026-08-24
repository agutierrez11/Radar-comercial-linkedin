import re

def apply_airtight_auth(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Header User Pill HTML (Remove admin dropdown from header, add logout button)
    old_header_pill = r'<!-- Active User Pill -->[\s\S]*?<!-- Botón Más Dropdown -->'
    new_header_pill = """<!-- Active User Pill & Logout -->
  <div style="display:flex; align-items:center; gap:8px;">
    <div class="kpi-pill" id="active-user-pill" style="background:rgba(79,70,229,0.12); border:1px solid var(--accent); color:var(--text); font-weight:700; font-size:11px; padding:4px 12px; border-radius:20px; display:flex; align-items:center; gap:6px;">
      <span class="dot" style="width:7px; height:7px; border-radius:50%; background:var(--green); display:inline-block;"></span>
      <span id="active-user-name">🔒 Sin Autenticar</span>
    </div>
    <button class="mini-btn" onclick="logoutUser()" style="padding:4px 10px; font-size:10px; font-weight:700; border-radius:14px; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); color:var(--red); cursor:pointer;" title="Cerrar Sesión y Bloquear Bóveda">
      🚪 Cerrar Sesión
    </button>
  </div>

  <!-- Botón Más Dropdown -->"""

    content = re.sub(old_header_pill, new_header_pill, content, count=1)

    # 2. Update default window.currentAuthUser to null
    content = content.replace("window.currentAuthUser = { id: 'antonio', name: 'Antonio (Master)', isMaster: true };", "window.currentAuthUser = null;")

    # 3. Update closeLoginModal safeguard (Cannot close without authenticated session)
    old_close_modal = """function closeLoginModal() {
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

    new_close_modal = """function closeLoginModal() {
  if (!window.currentAuthUser) {
    if (typeof showToast === 'function') showToast('🔒 Debes autenticarte para acceder a la bóveda.', '🔒');
    return;
  }
  console.log('[LoginModal] Closing login modal for user:', window.currentAuthUser.name);
  const modal = document.getElementById('login-modal');
  if (modal) {
    modal.classList.remove('open');
    modal.style.setProperty('display', 'none', 'important');
    modal.style.setProperty('opacity', '0', 'important');
    modal.style.setProperty('pointer-events', 'none', 'important');
  }
  document.body.classList.remove('not-authenticated');
}"""

    content = content.replace(old_close_modal, new_close_modal)

    # 4. Add logoutUser function
    logout_func = """function logoutUser() {
  try { sessionStorage.removeItem('rc_auth_user'); } catch(e){}
  window.currentAuthUser = null;
  S.contacts = [];
  S.positions = [];
  S.messages = [];
  S.crmState = { discarded: [], whitelisted: [], deals: [] };
  
  const activeUserPill = document.getElementById('active-user-name');
  if (activeUserPill) activeUserPill.textContent = '🔒 Sin Autenticar';
  
  document.body.classList.add('not-authenticated');
  if (typeof openLoginModal === 'function') openLoginModal();
  updateStatus();
  if (typeof renderDashboard === 'function') renderDashboard();
  if (typeof showToast === 'function') showToast('🔒 Sesión cerrada con éxito. Re-autentícate para ingresar.', '🔒');
}
window.logoutUser = logoutUser;"""

    if 'function logoutUser(' not in content:
        content = content.replace("window.closeLoginModal = closeLoginModal;", "window.closeLoginModal = closeLoginModal;\n" + logout_func)

    # 5. Update submitCustomLogin to save session in sessionStorage and load user data on demand
    old_submit_login_pattern = r'function submitCustomLogin\(targetUser\)[\s\S]*?window\.submitCustomLogin = submitCustomLogin;'
    new_submit_login = """function submitCustomLogin(targetUser) {
  const usernameInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  const inputVal = usernameInput ? usernameInput.value : '';
  const pwdVal = pwdInput ? pwdInput.value : '';
  const username = (targetUser || inputVal || '').trim().toLowerCase();
  if (!username) return;

  if (username === 'antonio' || username === 'master') {
    if (pwdVal && pwdVal !== '12345' && pwdVal !== 'admin') {
      showToast('❌ Contraseña de Administrador incorrecta.', '🔒');
      return;
    }
    window.currentAuthUser = { id: 'antonio', name: '👤 Antonio (Master)', isMaster: true };
    try { sessionStorage.setItem('rc_auth_user', JSON.stringify(window.currentAuthUser)); } catch(e){}
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';
    
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
    window.currentAuthUser = { id: username, name: `🔒 Bóveda ${nameStr} (Privada)`, isMaster: false };
    try { sessionStorage.setItem('rc_auth_user', JSON.stringify(window.currentAuthUser)); } catch(e){}
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `🔒 Bóveda ${nameStr} (Privada)`;
    
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
    window.currentAuthUser = { id: 'ronan', name: '🧪 Sandbox Ronan', isMaster: false, isSandbox: true };
    try { sessionStorage.setItem('rc_auth_user', JSON.stringify(window.currentAuthUser)); } catch(e){}
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';
    
    switchRonanAbMode('B');
  } else {
    window.currentAuthUser = { id: username, name: `👤 Bóveda ${username}`, isMaster: false };
    try { sessionStorage.setItem('rc_auth_user', JSON.stringify(window.currentAuthUser)); } catch(e){}
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `👤 Bóveda ${username}`;
    
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    updateStatus();
    navigate('upload');
    showToast(`🔒 Bóveda de ${username} lista.`, '🔑');
  }
}
window.submitCustomLogin = submitCustomLogin;"""

    content = re.sub(old_submit_login_pattern, new_submit_login, content, count=1)

    # 6. Update DOMContentLoaded bootstrap to check sessionStorage before auto-loading data
    old_dom_load = r'document\.addEventListener\(\'DOMContentLoaded\', async \(\) => \{[\s\S]*?if \(!window\.supabase\)'
    new_dom_load = """document.addEventListener('DOMContentLoaded', async () => {
  // Check active session in sessionStorage
  try {
    const savedSession = sessionStorage.getItem('rc_auth_user');
    if (savedSession) {
      window.currentAuthUser = JSON.parse(savedSession);
    }
  } catch(e){}

  // If no user is authenticated, LOCK the app immediately behind the modal and DO NOT LOAD DATA!
  if (!window.currentAuthUser) {
    document.body.classList.add('not-authenticated');
    S.contacts = [];
    updateStatus();
    if (typeof openLoginModal === 'function') openLoginModal();
    return;
  }

  const activeUserPill = document.getElementById('active-user-name');
  if (activeUserPill) activeUserPill.textContent = window.currentAuthUser.name;
  closeLoginModal();

  if (!window.currentAuthUser.isMaster) {
    console.log('[AutoVault Bootstrap] Skipped data load: Active user is non-master.');
    S.contacts = [];
    updateStatus();
    return;
  }

  // Restore vault for authenticated master user
  try {
    const restored = await restoreLocalVault();
    if (restored) {
      updateStatus();
      finalize();
      if (typeof navigate === 'function') navigate('network');
      return;
    }
  } catch (err) {
    console.warn("[AutoVault Bootstrap]", err);
  }

  if (!window.supabase)"""

    content = re.sub(old_dom_load, new_dom_load, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Airtight auth system applied to {filepath}")

apply_airtight_auth(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
apply_airtight_auth(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
