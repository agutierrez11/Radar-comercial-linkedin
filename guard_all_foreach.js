const fs = require('fs');

let html = fs.readFileSync('staging.html', 'utf8');

const targets = [
  { from: 'S.contacts.forEach', to: '(S.contacts || []).forEach' },
  { from: 'S.messages.forEach', to: '(S.messages || []).forEach' },
  { from: 'S.positions.forEach', to: '(S.positions || []).forEach' },
  { from: 'S.conversations.forEach', to: '(S.conversations || []).forEach' },
  { from: 'thread.messages.forEach', to: '(thread.messages || []).forEach' },
  { from: 'conv.msgs.forEach', to: '(conv.msgs || []).forEach' },
  { from: 'candidates.forEach', to: '(candidates || []).forEach' },
  { from: 'data.forEach', to: '(data || []).forEach' },
  { from: 'selected.forEach', to: '(selected || []).forEach' },
  { from: 'crmLeads.forEach', to: '(crmLeads || []).forEach' },
  { from: 'filteredContacts.forEach', to: '(filteredContacts || []).forEach' },
  { from: 'activeContacts.forEach', to: '(activeContacts || []).forEach' },
  { from: 'allContacts.forEach', to: '(allContacts || []).forEach' }
];

targets.forEach(t => {
  html = html.replaceAll(t.from, t.to);
});

fs.writeFileSync('staging.html', html, 'utf8');
console.log('✅ Safely guarded all state array forEach calls in staging.html');
