const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 7570; i <= 7650; i++) {
  console.log(`${i}: ${lines[i-1]}`);
}
