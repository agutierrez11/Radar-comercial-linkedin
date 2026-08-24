const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 3090; i <= 3160; i++) {
  console.log(`${i}: ${lines[i-1]}`);
}
