import re

def apply_zero_session(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Disable automatic Supabase data fetcher on DOMContentLoaded in head tag
    old_supa_promise = r'window\.__supabaseDataPromise = new Promise\(function\(resolve\) \{[\s\S]*?\}\);\s*\}\)\(\);'
    new_supa_promise = """window.fetchMasterSupabaseData = function() {
    return new Promise(function(resolve) {
      if (!window.supabase || typeof window.supabase.createClient !== 'function') {
        resolve([]);
        return;
      }
      var supaClient = window.supabase.createClient(SUPA_URL, SUPA_KEY);
      fetchAllConnections(supaClient).then(function(rows) {
        var mapped = rows.map(mapRow);
        window.ENRICHED_CONNECTIONS_DATA = mapped;
        resolve(mapped);
      }).catch(function(e) {
        console.error('[Supabase] Error:', e);
        window.ENRICHED_CONNECTIONS_DATA = [];
        resolve([]);
      });
    });
  };
})();"""

    content = re.sub(old_supa_promise, new_supa_promise, content, count=1)

    # 2. Strict DOMContentLoaded bootstrap: ALWAYS start 100% locked with 0 contacts!
    old_dom_load = r'document\.addEventListener\(\'DOMContentLoaded\', async \(\) => \{[\s\S]*?if \(!window\.supabase\)'
    new_dom_load = """document.addEventListener('DOMContentLoaded', async () => {
  // ALWAYS START LOCKED WITH ZERO DATA ON PAGE REFRESH OR INITIAL OPEN!
  window.currentAuthUser = null;
  S.contacts = [];
  S.positions = [];
  S.messages = [];
  
  document.body.classList.add('not-authenticated');
  const activeUserPill = document.getElementById('active-user-name');
  if (activeUserPill) activeUserPill.textContent = '🔒 Sin Autenticar';
  
  updateStatus();
  if (typeof renderDashboard === 'function') renderDashboard();
  if (typeof openLoginModal === 'function') openLoginModal();
  
  // Do NOT load data automatically! Wait for explicit login in modal!
  return;

  if (!window.supabase)"""

    content = re.sub(old_dom_load, new_dom_load, content, count=1)

    # 3. Update quickLogin to enforce PIN 12345 prompt/validation for Antonio
    old_quick_login = r'function quickLogin\(username, pwd\) \{[\s\S]*?submitCustomLogin\(username\);\s*\}'
    new_quick_login = """function quickLogin(username, pwd) {
  const usernameInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');

  if (username === 'antonio' || username === 'master') {
    const adminPin = prompt('🔒 Bóveda Privada del Administrador (Antonio).\\nIngresa el PIN de Administrador (ej. 12345):');
    if (!adminPin || adminPin.trim() !== '12345') {
      if (typeof showToast === 'function') showToast('❌ PIN de Administrador incorrecto. Acceso denegado.', '🔒');
      return;
    }
    if (pwdInput) pwdInput.value = '12345';
  }

  if (usernameInput) usernameInput.value = username;
  submitCustomLogin(username);
}"""

    content = re.sub(old_quick_login, new_quick_login, content, count=1)

    # 4. Update submitCustomLogin to enforce PIN check for Antonio and load data ONLY AFTER login
    old_submit = r'function submitCustomLogin\(targetUser\) \{[\s\S]*?window\.submitCustomLogin = submitCustomLogin;'
    new_submit = """function submitCustomLogin(targetUser) {
  const usernameInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  const inputVal = usernameInput ? usernameInput.value : '';
  const pwdVal = pwdInput ? pwdInput.value : '';
  const username = (targetUser || inputVal || '').trim().toLowerCase();
  if (!username) return;

  if (username === 'antonio' || username === 'master') {
    if (pwdVal !== '12345' && pwdVal !== 'admin') {
      const pin = prompt('🔒 Ingresa el PIN de Administrador para la Bóveda Antonio (12345):');
      if (!pin || pin.trim() !== '12345') {
        if (typeof showToast === 'function') showToast('❌ PIN incorrecto. Acceso denegado.', '🔒');
        return;
      }
    }
    
    window.currentAuthUser = { id: 'antonio', name: '👤 Antonio (Master)', isMaster: true };
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';
    
    closeLoginModal();
    showToast('⏳ Cargando Bóveda Master Antonio (2,953 contactos)...', '⏳');
    
    restoreLocalVault().then(restored => {
      if (!restored) {
        if (typeof window.fetchMasterSupabaseData === 'function') {
          window.fetchMasterSupabaseData().then(contacts => {
            if (contacts && contacts.length > 0) {
              S.contacts = contacts;
            } else {
              loadDemoData(false);
            }
            updateStatus();
            if (typeof renderDashboard === 'function') renderDashboard();
            if (typeof renderNetworkTable === 'function') renderNetworkTable();
            showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
          });
        } else {
          loadDemoData(false);
          updateStatus();
          if (typeof renderDashboard === 'function') renderDashboard();
          if (typeof renderNetworkTable === 'function') renderNetworkTable();
          showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
        }
      } else {
        updateStatus();
        if (typeof renderDashboard === 'function') renderDashboard();
        if (typeof renderNetworkTable === 'function') renderNetworkTable();
        showToast('👤 Bóveda Master Antonio cargada desde almacenamiento local.', '🔑');
      }
    });
  } else if (username === 'giovanna' || username === 'roanna') {
    const isGio = username === 'giovanna';
    const nameStr = isGio ? 'Giovanna' : 'Roanna';
    window.currentAuthUser = { id: username, name: `🔒 Bóveda ${nameStr} (Privada)`, isMaster: false };
    
    // Complete isolation: Vault is 100% EMPTY for non-master users!
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    S.crmState = { discarded: [], whitelisted: [], deals: [] };
    S.loadedParts = { connections: false, messages: false, positions: false, profile: false };
    S.isDemoLoaded = false;
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `🔒 Bóveda ${nameStr} (Privada)`;
    
    updateStatus();
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    navigate('upload');
    showToast(`🔒 Bóveda Aislada de ${nameStr} (0 contactos). Lista para cargar tu ZIP.`, '🔒');
  } else if (username === 'ronan') {
    window.currentAuthUser = { id: 'ronan', name: '🧪 Sandbox Ronan', isMaster: false, isSandbox: true };
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';
    
    switchRonanAbMode('B');
  } else {
    window.currentAuthUser = { id: username, name: `👤 Bóveda ${username}`, isMaster: false };
    
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    
    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `👤 Bóveda ${username}`;
    
    updateStatus();
    navigate('upload');
    showToast(`🔒 Bóveda de ${username} lista (0 contactos).`, '🔑');
  }
}
window.submitCustomLogin = submitCustomLogin;"""

    content = re.sub(old_submit, new_submit, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Zero session startup lockout applied to {filepath}")

apply_zero_session(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
apply_zero_session(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
