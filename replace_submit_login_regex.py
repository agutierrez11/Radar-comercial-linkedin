import re

def replace_regex(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pristine_func = """function submitCustomLogin(targetUser) {
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
    window.currentAuthUser = { id: 'antonio', name: '👤 Antonio (Master)', isMaster: true };
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';
    if (activePillContainer) { activePillContainer.style.cursor = 'pointer'; }
    if (adminDropdown) adminDropdown.style.display = 'block';
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
    window.currentAuthUser = { id: username, name: `🔒 Bóveda ${nameStr} (Privada)`, isMaster: false };
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
    window.currentAuthUser = { id: 'ronan', name: '🧪 Sandbox Ronan', isMaster: false, isSandbox: true };
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';
    if (activePillContainer) { activePillContainer.style.cursor = 'default'; activePillContainer.onclick = null; }
    if (adminDropdown) adminDropdown.style.display = 'none';
    if (ronanBanner) ronanBanner.style.display = 'flex';
    
    switchRonanAbMode('B');
  } else {
    window.currentAuthUser = { id: username, name: `👤 Bóveda ${username}`, isMaster: false };
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
}
window.submitCustomLogin = submitCustomLogin;"""

    pattern = r'function submitCustomLogin\(targetUser\)[\s\S]*?window\.submitCustomLogin = submitCustomLogin;'
    # Replace all occurrences of submitCustomLogin with pristine_func
    new_content, count = re.subn(pattern, pristine_func, content)
    print(f"Replaced {count} occurrences in {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

replace_regex(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
replace_regex(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
