const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 8080; i < lines.length; i++) {
  console.log(`${i+1}: ${lines[i]}`);
}
