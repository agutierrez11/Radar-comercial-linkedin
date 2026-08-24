const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 6370; i <= 6420; i++) {
  if (lines[i-1]) console.log(`${i}: ${lines[i-1]}`);
}
