const fs = require('fs');

function fixVaultSwitchingInFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');

  const newSubmitCustomLogin = `async function submitCustomLogin(targetUser) {
  const usernameInput = document.getElementById('login-username-input');
  const inputVal = usernameInput ? usernameInput.value : '';
  const username = (targetUser || inputVal || '').trim().toLowerCase();
  if (!username) return;

  closeLoginModal();
  const activeUserPill = document.getElementById('active-user-name');
  const ronanBanner = document.getElementById('ronan-ab-banner');

  // Reset memory state completely before loading targeted vault
  S.contacts = [];
  S.positions = [];
  S.messages = [];
  S.filteredContacts = [];
  S.purgeChecked = new Set();
  S.loadedParts = { connections: false, positions: false, messages: false, profile: false };

  if (username === 'antonio' || username === 'master') {
    window.currentAuthUser = { id: 'antonio', name: 'Antonio (Master)', isMaster: true };
    if (activeUserPill) activeUserPill.textContent = '👤 Antonio (Master)';
    if (ronanBanner) ronanBanner.style.display = 'none';

    // Force clean reload of Antonio's Master Vault (2,953 contacts + 25,110 messages)
    if (typeof loadDemoData === 'function') {
      await loadDemoData(true);
    }
    showToast('👤 Bóveda Master Antonio cargada (2,953 contactos activos).', '🔑');

  } else if (username === 'giovanna') {
    window.currentAuthUser = { id: 'giovanna', name: 'Giovanna (Bóveda Aislada)', isMaster: false };
    if (activeUserPill) activeUserPill.textContent = '👤 Giovanna (Bóveda Aislada)';
    if (ronanBanner) ronanBanner.style.display = 'none';

    // Giovanna Isolated Vault: Check localStorage or keep 100% clean
    const savedGiovanna = localStorage.getItem('vault_giovanna');
    if (savedGiovanna) {
      try {
        const parsed = JSON.parse(savedGiovanna);
        S.contacts = parsed.contacts || [];
        S.positions = parsed.positions || [];
        S.messages = parsed.messages || [];
        S.loadedParts = { connections: S.contacts.length > 0, messages: S.messages.length > 0 };
        showToast(\`🔒 Bóveda de Giovanna restaurada (\${S.contacts.length} contactos).\`, '🔒');
      } catch(e) {
        showToast('🔒 Bóveda de Giovanna inicializada (Vacía). Lista para cargar tu ZIP.', '🔒');
      }
    } else {
      showToast('🔒 Bóveda de Giovanna seleccionada (0 contactos). Lista para cargar tu ZIP.', '🔒');
    }
    navigate('upload');

  } else if (username === 'ronan') {
    window.currentAuthUser = { id: 'ronan', name: 'Sandbox Demo Ronan', isMaster: false, isSandbox: true };
    if (activeUserPill) activeUserPill.textContent = '🧪 Sandbox Ronan';
    if (ronanBanner) ronanBanner.style.display = 'flex';

    if (typeof switchRonanAbMode === 'function') {
      switchRonanAbMode('B');
    }
    navigate('network');
    showToast('🧪 Sandbox Demo Ronan: Bóveda Demo (500 contactos) activada.', '🧪');

  } else {
    window.currentAuthUser = { id: username, name: username.charAt(0).toUpperCase() + username.slice(1), isMaster: false };
    if (activeUserPill) activeUserPill.textContent = \`👤 \${window.currentAuthUser.name}\`;
    if (ronanBanner) ronanBanner.style.display = 'none';
    navigate('upload');
    showToast(\`👤 Bóveda de \${window.currentAuthUser.name} inicializada (Vacía).\`, '👤');
  }

  // Update UI and badges for switched vault
  if (typeof updateStatus === 'function') updateStatus();
  if (typeof renderHeader === 'function') renderHeader();
  if (typeof renderDashboard === 'function') renderDashboard();
  if (typeof renderNetworkTable === 'function') renderNetworkTable();
}`;

  const submitLoginRegex = /async?\s+function submitCustomLogin\(targetUser\)\s*\{[\s\S]*?\n\}/g;
  html = html.replace(submitLoginRegex, newSubmitCustomLogin);

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`✅ Fixed submitCustomLogin vault switching in ${filePath}`);
}

fixVaultSwitchingInFile('staging.html');
fixVaultSwitchingInFile('index.html');
