const fs = require('fs');
const lines = fs.readFileSync('staging.html', 'utf8').split('\n');

for (let i = 3120; i <= 3165; i++) {
  console.log(`${i}: ${lines[i-1]}`);
}
