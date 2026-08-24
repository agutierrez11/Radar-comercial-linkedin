const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 7680; i <= 7735; i++) {
  if (lines[i-1]) console.log(`${i}: ${lines[i-1]}`);
}
