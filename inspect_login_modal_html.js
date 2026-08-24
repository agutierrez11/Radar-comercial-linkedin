const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('login-modal')) {
    console.log(`${i+1}: ${lines[i].trim().substring(0, 100)}`);
  }
}
