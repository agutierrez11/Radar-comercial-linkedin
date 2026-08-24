const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

const start = lines.findIndex(l => l.includes('function navigate(sec)'));
for (let i = start; i < start + 50; i++) {
  console.log(`${i+1}: ${lines[i]}`);
}
