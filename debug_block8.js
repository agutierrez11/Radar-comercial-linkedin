const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptRegex = /<script>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  if (count === 8) {
    const code = match[1];
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
      try {
        new Function(lines.slice(0, i + 1).join('\n'));
      } catch (e) {
        if (!e.message.includes('Unexpected end of input') && !e.message.includes('Missing')) {
          console.log(`Block 8 Line ${i+1}: ${e.message} --> ${lines[i].trim()}`);
        }
      }
    }
  }
}
