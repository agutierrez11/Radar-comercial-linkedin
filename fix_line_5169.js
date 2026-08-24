const fs = require('fs');

let html = fs.readFileSync('staging.html', 'utf8');

// Replace conversations.forEach with (S.conversations || []).forEach
html = html.replace('conversations.forEach(thread => {', '(S.conversations || []).forEach(thread => {');

// Ensure S state has conversations: []
if (!html.includes('conversations: []')) {
  html = html.replace('contacts: [],', 'contacts: [],\n    conversations: [],');
}

fs.writeFileSync('staging.html', html, 'utf8');
console.log('✅ Replaced line 5169 conversations.forEach in staging.html');
