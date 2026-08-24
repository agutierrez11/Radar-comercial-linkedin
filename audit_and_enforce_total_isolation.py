import re

def apply_isolation_audit(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add anti-cache headers in head tag
    anti_cache_meta = """  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">"""
    
    if "must-revalidate" not in content:
        content = content.replace("<head>", f"<head>\n{anti_cache_meta}")

    # 2. Add resetGlobalState helper function
    reset_state_fn = """function resetGlobalState() {
  S.contacts = [];
  S.messages = [];
  S.positions = [];
  S.filteredContacts = [];
  S.conversations = [];
  S.purgeChecked = new Set();
  S.expandedChats = new Set();
  S.crmState = { discarded: [], whitelisted: [], deals: [] };
  S.loadedParts = { connections: false, messages: false, positions: false, profile: false };
  S.ownerName = '';
  window.ENRICHED_CONNECTIONS_DATA = [];
}
window.resetGlobalState = resetGlobalState;"""

    if "function resetGlobalState()" not in content:
        content = content.replace("const S = window.S = {", f"{reset_state_fn}\n\nconst S = window.S = {{")

    # 3. Update restoreLocalVault to strictly block non-master users from restoring local IndexedDB/localStorage vault
    old_restore = r'async function restoreLocalVault\(\) \{'
    new_restore = """async function restoreLocalVault() {
  if (!window.currentAuthUser || !window.currentAuthUser.isMaster) {
    console.log('[AutoVault] Ignorado: El usuario activo no es Master Admin.');
    return false;
  }"""
    content = re.sub(old_restore, new_restore, content, count=1)

    # 4. Update submitCustomLogin to execute resetGlobalState() FIRST and set S.ownerName appropriately
    old_submit = r'function submitCustomLogin\(\) \{[\s\S]*?window\.submitCustomLogin = submitCustomLogin;'
    
    new_submit = """function submitCustomLogin() {
  const userInput = document.getElementById('login-username-input');
  const pwdInput = document.getElementById('login-password-input');
  const alertDiv = document.getElementById('login-error-alert');
  if (alertDiv) alertDiv.style.display = 'none';

  const userVal = (userInput ? userInput.value : '').trim().toLowerCase();
  const pwdVal = (pwdInput ? pwdInput.value : '').trim();

  if (!userVal) {
    if (alertDiv) {
      alertDiv.textContent = '⚠️ Ingresa tu usuario o email.';
      alertDiv.style.display = 'block';
    }
    return;
  }

  // --- MANDATORY ZERO-DATA RESET BEFORE SWITCHING TENANTS ---
  resetGlobalState();

  // --- ANTONIO MASTER ADMIN ---
  if (userVal === 'antonio' || userVal === 'antonio@radar.com' || userVal === 'master') {
    if (pwdVal !== '12345' && pwdVal !== 'admin') {
      if (alertDiv) {
        alertDiv.textContent = '❌ PIN o Contraseña incorrecta para Antonio Master.';
        alertDiv.style.display = 'block';
      }
      if (typeof showToast === 'function') showToast('❌ PIN o Contraseña incorrecta.', '🔒');
      return;
    }

    window.currentAuthUser = { id: 'antonio', name: '👤 Antonio (Master)', isMaster: true };
    S.ownerName = "Antonio Gutiérrez";
    S.positions = [
      { company: "Clip", title: "Acquisition Executive | BDR | Sales", start: "Jul 2021", end: "Mar 2025" },
      { company: "Fiserv", title: "Business Sales Consultant", start: "Mar 2024", end: "Oct 2025" },
      { company: "LATAM Commerce", title: "Co-creador", start: "Mar 2024", end: "Actual" },
      { company: "ENFA DELIVERY", title: "Ejecutivo de desarrollo del negocio", start: "Jul 2020", end: "Oct 2020" },
      { company: "JTI (Japan Tobacco International)", title: "Ejecutivo Desarrollador Canal HORECA", start: "Jul 2018", end: "Dec 2019" },
      { company: "Conagra Brands", title: "Ejecutivo de ventas", start: "2016", end: "2018" }
    ];

    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';

    closeLoginModal();
    if (typeof showToast === 'function') showToast('⏳ Cargando Bóveda Master Antonio (2,953 contactos)...', '⏳');

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
            if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
          });
        } else {
          loadDemoData(false);
          updateStatus();
          if (typeof renderDashboard === 'function') renderDashboard();
          if (typeof renderNetworkTable === 'function') renderNetworkTable();
          if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');
        }
      } else {
        updateStatus();
        if (typeof renderDashboard === 'function') renderDashboard();
        if (typeof renderNetworkTable === 'function') renderNetworkTable();
        if (typeof showToast === 'function') showToast('👤 Bóveda Master Antonio cargada desde almacenamiento local.', '🔑');
      }
    });
  } 
  // --- GIOVANNA ISOLATED VAULT ---
  else if (userVal === 'giovanna' || userVal === 'giovanna@radar.com' || userVal === 'roanna') {
    if (pwdVal !== 'gio2026' && pwdVal !== '12345' && pwdVal !== 'giovanna') {
      if (alertDiv) {
        alertDiv.textContent = '❌ Contraseña incorrecta para Bóveda Giovanna.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    const isGio = userVal.includes('giovanna');
    const nameStr = isGio ? 'Giovanna' : 'Roanna';
    window.currentAuthUser = { id: userVal, name: `🔒 Bóveda ${nameStr} (Privada)`, isMaster: false };
    S.ownerName = nameStr;

    // Zero-data state for Giovanna
    S.contacts = [];
    S.positions = [];
    S.messages = [];
    S.crmState = { discarded: [], whitelisted: [], deals: [] };
    S.loadedParts = { connections: false, messages: false, positions: false, profile: false };

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `🔒 Bóveda ${nameStr} (Privada)`;

    updateStatus();
    if (typeof renderDashboard === 'function') renderDashboard();
    if (typeof renderNetworkTable === 'function') renderNetworkTable();
    if (typeof navigate === 'function') navigate('upload');
    if (typeof showToast === 'function') showToast(`🔒 Bóveda Aislada de ${nameStr} (0 contactos). Lista para cargar tu ZIP.`, '🔒');
  } 
  // --- RONAN SANDBOX ---
  else if (userVal === 'ronan' || userVal === 'ronan@radar.com') {
    if (pwdVal !== 'ronan123' && pwdVal !== '12345' && pwdVal !== 'ronan') {
      if (alertDiv) {
        alertDiv.textContent = '❌ Contraseña incorrecta para Sandbox Ronan.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    window.currentAuthUser = { id: 'ronan', name: '🧪 Sandbox Ronan', isMaster: false, isSandbox: true };
    S.ownerName = 'Ronan';
    S.positions = [];
    S.messages = []; // Clear Antonio's messages!

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';

    if (typeof switchRonanAbMode === 'function') switchRonanAbMode('B');
  } 
  // --- OTHER INDIVIDUAL USERS ---
  else {
    if (!pwdVal) {
      if (alertDiv) {
        alertDiv.textContent = '⚠️ Ingresa una contraseña para tu bóveda.';
        alertDiv.style.display = 'block';
      }
      return;
    }

    window.currentAuthUser = { id: userVal, name: `👤 Bóveda ${userVal}`, isMaster: false };
    S.ownerName = userVal;
    S.contacts = [];
    S.positions = [];
    S.messages = [];

    closeLoginModal();
    const activeUserPill = document.getElementById('active-user-name');
    if (activeUserPill) activeUserPill.textContent = `👤 Bóveda ${userVal}`;

    updateStatus();
    if (typeof navigate === 'function') navigate('upload');
    if (typeof showToast === 'function') showToast(`🔒 Bóveda de ${userVal} lista (0 contactos).`, '🔑');
  }
}
window.submitCustomLogin = submitCustomLogin;"""

    content = re.sub(old_submit, new_submit, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Total tenant isolation audit applied to {filepath}")

apply_isolation_audit(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
apply_isolation_audit(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
