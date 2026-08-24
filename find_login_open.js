const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 7550; i <= 7590; i++) {
  if (lines[i-1]) console.log(`${i}: ${lines[i-1]}`);
}
