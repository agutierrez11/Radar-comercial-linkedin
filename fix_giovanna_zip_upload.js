const fs = require('fs');

function enableUserZipStorage(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');

  // New clean saveLocalVault allowing all non-demo users (like giovanna) to save
  const newSaveLocalVault = `async function saveLocalVault() {
  if (!S.contacts || S.contacts.length === 0 || S.isDemoLoaded) return;
  const userId = (window.currentAuthUser && window.currentAuthUser.id) ? window.currentAuthUser.id : 'antonio';
  if (userId === 'ronan') return; // Do not auto-overwrite demo sandbox

  try {
    const db = await openVaultDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const dataToSave = {
      timestamp: new Date().toISOString(),
      ownerName: S.ownerName || userId,
      contacts: S.contacts,
      positions: S.positions || [],
      messages: S.messages || []
    };
    const vaultKey = getVaultKey();
    store.put(dataToSave, vaultKey);
    localStorage.setItem(vaultKey, JSON.stringify(dataToSave));
    console.log(\`[AutoVault] Bóveda guardada para \${vaultKey} (\${S.contacts.length} contactos).\`);
    
    // Cloud sync to Supabase if connected
    if (typeof syncToSupabaseVault === 'function') {
      syncToSupabaseVault(userId, S.contacts);
    }
  } catch (err) {
    console.warn('[AutoVault Save Error]', err);
  }
}`;

  // New clean restoreLocalVault allowing user specific restore
  const newRestoreLocalVault = `async function restoreLocalVault() {
  try {
    const userId = (window.currentAuthUser && window.currentAuthUser.id) ? window.currentAuthUser.id : 'antonio';
    if (userId === 'ronan') return false; // Ronan always uses sandbox demo

    // Try IndexedDB first
    const vaultKey = getVaultKey();
    try {
      const db = await openVaultDB();
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const request = store.get(vaultKey);
      const data = await new Promise((resolve, reject) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });

      if (data && data.contacts && data.contacts.length > 0) {
        S.contacts = data.contacts;
        S.positions = data.positions || [];
        S.messages = data.messages || [];
        S.ownerName = data.ownerName || userId;
        S.loadedParts = { connections: true, positions: S.positions.length > 0, messages: S.messages.length > 0 };
        console.log(\`[AutoVault] Bóveda \${vaultKey} restaurada desde IndexedDB (\${S.contacts.length} contactos).\`);
        return true;
      }
    } catch (idbErr) {
      console.warn('[AutoVault IDB Error]', idbErr);
    }

    // Fallback to localStorage
    const savedLocal = localStorage.getItem(vaultKey);
    if (savedLocal) {
      const data = JSON.parse(savedLocal);
      if (data && data.contacts && data.contacts.length > 0) {
        S.contacts = data.contacts;
        S.positions = data.positions || [];
        S.messages = data.messages || [];
        S.ownerName = data.ownerName || userId;
        S.loadedParts = { connections: true, positions: S.positions.length > 0, messages: S.messages.length > 0 };
        console.log(\`[AutoVault] Bóveda \${vaultKey} restaurada desde localStorage (\${S.contacts.length} contactos).\`);
        return true;
      }
    }

    return false;
  } catch (err) {
    console.warn('[AutoVault Restore Error]', err);
    return false;
  }
}`;

  const saveRegex = /async?\s+function saveLocalVault\(\)\s*\{[\s\S]*?\n\}/g;
  const restoreRegex = /async?\s+function restoreLocalVault\(\)\s*\{[\s\S]*?\n\}/g;

  html = html.replace(saveRegex, newSaveLocalVault);
  html = html.replace(restoreRegex, newRestoreLocalVault);

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`✅ Enabled ZIP upload, saving & restore for Giovanna and all users in ${filePath}`);
}

enableUserZipStorage('staging.html');
enableUserZipStorage('index.html');
