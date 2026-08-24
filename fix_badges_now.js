const fs = require('fs');

function updateFileBadges(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');

  // New robust renderHeader function
  const updatedRenderHeader = `function renderHeader() {
  const setEl = (id, fn) => { const el = document.getElementById(id); if (el) fn(el); };
  const activeContacts = (S.contacts || []).filter(c => c.crmStatus !== 'Descartado' && !c.discardedFromPurge);
  const total = activeContacts.length;
  const clevel = activeContacts.filter(c => c.hierarchy === 'C-Level').length;
  const countries = new Set(activeContacts.filter(c => c.country !== 'Desconocido').map(c => c.country)).size;
  const classa = activeContacts.filter(c => c.score >= 60).length;

  // Header KPIs
  setEl('hkpi-total', el => el.textContent = total.toLocaleString());
  setEl('hkpi-clevel', el => el.textContent = clevel);
  setEl('hkpi-countries', el => el.textContent = countries);

  // Sidebar Badges
  setEl('nb-network', el => el.textContent = total > 0 ? total.toLocaleString() : '-');
  setEl('nb-icp', el => el.textContent = classa > 0 ? classa.toLocaleString() : '-');

  const purgeCount = (S.contacts || []).filter(c => typeof isPurgeCandidate === 'function' && isPurgeCandidate(c)).length;
  setEl('nb-purge', el => el.textContent = purgeCount > 0 ? purgeCount.toLocaleString() : '-');

  const crmCount = (S.contacts || []).filter(c => c.crmStatus && c.crmStatus !== 'Ninguno' && c.crmStatus !== 'Descartado').length;
  setEl('nb-crm', el => el.textContent = crmCount);

  // Dunbar Bar
  const dunbarPct = Math.min(100, (classa / 150) * 100);
  setEl('dunbar-fill', el => {
    el.style.width = dunbarPct + '%';
    el.style.background = classa > 150 ? 'var(--amber)' : 'var(--green)';
  });
  setEl('dunbar-label', el => el.textContent = \`\${classa}/150\`);
  setEl('header-kpis', el => el.style.display = 'flex');

  // Messages Badge (2,088 conversations / messages)
  const convSet = new Set();
  if (S.messages && S.messages.length > 0) {
    S.messages.forEach(m => {
      const cid = m.conv_id || m['CONVERSATION ID'] || m.CONVERSATION_ID || m.FROM || m.SENDER_NAME;
      if (cid) convSet.add(cid);
    });
  }
  const msgsCount = convSet.size > 0 ? convSet.size : ((S.contacts || []).filter(c => c.msg_count && c.msg_count > 0).length);
  setEl('nb-msgs', el => el.textContent = msgsCount > 0 ? msgsCount.toLocaleString() : '-');
}`;

  const renderHeaderRegex = /function renderHeader\(\)\s*\{[\s\S]*?\n\}/g;
  html = html.replace(renderHeaderRegex, updatedRenderHeader);

  // Also make sure loadDemoData / finalize calls renderHeader()
  if (html.includes('finalize() {') && !html.includes('renderHeader();')) {
    html = html.replace('function finalize() {', 'function finalize() {\n  renderHeader();');
  }

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`✅ Updated badges logic in ${filePath}`);
}

updateFileBadges('staging.html');
updateFileBadges('index.html');
