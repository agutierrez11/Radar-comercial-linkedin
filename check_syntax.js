const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptRegex = /<script>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  try {
    new Function(match[1]);
    console.log(`Script block #${count}: SYNTAX OK`);
  } catch (err) {
    console.error(`Script block #${count}: SYNTAX ERROR:`, err.message);
  }
}
