const fs = require('fs');

let content = fs.readFileSync('staging.html', 'utf8');

// Replace the broken popupContent block
const target = `<div>👑 <strong>C-Level:</strong> <span style="color:#c084fc;">\${cLevels}</span></div>
          <div>🎯 <strong>Directores:</strong> <span style="color:#60a5fa;">\${directors}</span></div>
          <div>"// ═══════════════════════════════════════════════════════════════════════`;

const replacement = `<div>👑 <strong>C-Level:</strong> <span style="color:#c084fc;">\${cLevels}</span></div>
          <div>🎯 <strong>Directores:</strong> <span style="color:#60a5fa;">\${directors}</span></div>
          <div>💼 <strong>Gerentes:</strong> <span style="color:#34d399;">\${managers}</span></div>
        </div>
      </div>
    \`;

// ═══════════════════════════════════════════════════════════════════════`;

if (content.includes('<div>"// ═══')) {
  content = content.replace(target, replacement);
  fs.writeFileSync('staging.html', content, 'utf8');
  console.log('✅ Fixed syntax error on line 3146 of staging.html');
} else {
  console.log('Target string not found, checking exact lines...');
}
