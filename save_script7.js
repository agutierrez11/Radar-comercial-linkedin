const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptRegex = /<script>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  if (count === 7) {
    const code = match[1];
    fs.writeFileSync('temp_script7.js', code, 'utf8');
    console.log('Script 7 written to temp_script7.js');
  }
}
