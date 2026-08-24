const fs = require('fs');

let html = fs.readFileSync('staging.html', 'utf8');

// 1. Safe renderHeader
const safeRenderHeader = `function renderHeader() {
  const setEl = (id, fn) => { const el = document.getElementById(id); if (el) fn(el); };
  const activeContacts = (S.contacts || []).filter(c => c.crmStatus !== 'Descartado' && !c.discardedFromPurge);
  const total = activeContacts.length;
  const clevel = activeContacts.filter(c => c.hierarchy === 'C-Level').length;
  const countries = new Set(activeContacts.filter(c => c.country !== 'Desconocido').map(c => c.country)).size;
  const classa = activeContacts.filter(c => c.score >= 60).length;
  setEl('hkpi-total', el => el.textContent = total.toLocaleString());
  setEl('hkpi-clevel', el => el.textContent = clevel);
  setEl('hkpi-countries', el => el.textContent = countries);
  const dunbarPct = Math.min(100, (classa / 150) * 100);
  setEl('dunbar-fill', el => {
    el.style.width = dunbarPct + '%';
    el.style.background = classa > 150 ? 'var(--amber)' : 'var(--green)';
  });
  setEl('dunbar-label', el => el.textContent = \`\${classa}/150\`);
  setEl('header-kpis', el => el.style.display = 'flex');
}`;

const renderHeaderRegex = /function renderHeader\(\)\s*\{[\s\S]*?\n\}/g;
html = html.replace(renderHeaderRegex, safeRenderHeader);

// 2. Define toggleMoreMenu and closeConfigModal globally in main script
if (!html.includes('window.toggleMoreMenu =')) {
  const globalHelpers = `
  window.toggleMoreMenu = function(e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('more-menu-dropdown');
    if (menu) {
      menu.style.display = (menu.style.display === 'none' || !menu.style.display) ? 'block' : 'none';
    }
  };
  window.closeConfigModal = function() {
    const menu = document.getElementById('more-menu-dropdown');
    if (menu) menu.style.display = 'none';
  };
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('more-menu-dropdown');
    const btn = document.getElementById('more-menu-btn');
    if (menu && btn && !menu.contains(e.target) && !btn.contains(e.target)) {
      menu.style.display = 'none';
    }
  });
`;
  html = html.replace('function navigate(sec) {', globalHelpers + '\nfunction navigate(sec) {');
}

// 3. Fix conversations variable usage
html = html.replace(/\bconversations\b/g, '(S.messages || [])');

fs.writeFileSync('staging.html', html, 'utf8');
console.log('✅ Applied safe fixes to staging.html');
