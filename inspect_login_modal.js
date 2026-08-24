const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 7450; i <= 7650; i++) {
  if (lines[i-1] && (lines[i-1].includes('login') || lines[i-1].includes('Vault') || lines[i-1].includes('select') || lines[i-1].includes('switch') || lines[i-1].includes('Giovanna') || lines[i-1].includes('Ronan') || lines[i-1].includes('Antonio'))) {
    console.log(`${i}: ${lines[i-1].trim().substring(0, 120)}`);
  }
}
