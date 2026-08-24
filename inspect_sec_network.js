const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 1015; i <= 1060; i++) {
  if (lines[i-1]) console.log(`${i}: ${lines[i-1]}`);
}
