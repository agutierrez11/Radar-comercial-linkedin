const fs = require('fs');
const lines = fs.readFileSync('staging.html', 'utf8').split('\n');

for (let i = 3195; i <= 3215; i++) {
  console.log(`${i}: ${lines[i-1]}`);
}
