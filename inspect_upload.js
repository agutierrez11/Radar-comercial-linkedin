const fs = require('fs');
const lines = fs.readFileSync('index.html', 'utf8').split('\n');

for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('id="sec-upload"')) {
    console.log(`Found sec-upload at line ${i+1}`);
    for (let j = i; j < i + 80; j++) {
      console.log(`${j+1}: ${lines[j]}`);
    }
    break;
  }
}
