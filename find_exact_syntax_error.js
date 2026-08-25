const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scriptRegex = /<script>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  if (count === 7) {
    const code = match[1];
    try {
      new Function(code);
      console.log("Script 7 compiles clean!");
    } catch(e) {
      console.error("Script 7 error:", e.message);
      // Binary search for error line
      const lines = code.split('\n');
      for (let i = 1; i <= lines.length; i++) {
        try {
          new Function(lines.slice(0, i).join('\n'));
        } catch(err) {
          if (!err.message.includes('Unexpected end of input') && !err.message.includes('Missing }') && !err.message.includes('unexpected token \')\'')) {
            console.log(`Error at chunk up to line ${i}: ${err.message}`);
            console.log(`Line ${i}: ${lines[i-1]}`);
            break;
          }
        }
      }
    }
  }
}
