const fs = require('fs');

let content = fs.readFileSync('staging.html', 'utf8');

const oldChunk = `          <div>🎯 <strong>Directores:</strong> <span style="color:#60a5fa;">\${directors}</span></div>
          <div>"// ═══════════════════════════════════════════════════════════════════════`;

// Search for the exact line index
const lines = content.split('\n');
let targetLineIndex = -1;

for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('<div>"// ═══')) {
    targetLineIndex = i;
    break;
  }
}

if (targetLineIndex !== -1) {
  console.log(`Found broken syntax at line ${targetLineIndex + 1}: ${lines[targetLineIndex]}`);
  lines[targetLineIndex] = `          <div>💼 <strong>Gerentes:</strong> <span style="color:#34d399;">\${managers}</span></div>\n        </div>\n      </div>\n    \`;\n\n// ═══════════════════════════════════════════════════════════════════════`;
  fs.writeFileSync('staging.html', lines.join('\n'), 'utf8');
  console.log('✅ Successfully fixed syntax error on staging.html');
} else {
  console.error('❌ Could not find line with <div>"// ═══');
}
