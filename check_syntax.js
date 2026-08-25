const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;

let match;
let count = 0;
let errors = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  const code = match[1];
  if (!code.trim()) continue;
  try {
    new vm.Script(code);
  } catch (err) {
    errors++;
    console.error(`❌ Syntax Error in Script block ${count}:`, err.message);
  }
}

if (errors === 0) {
  console.log(`✅ ALL ${count} SCRIPT BLOCKS PASSED SYNTAX CHECK CLEANLY!`);
  process.exit(0);
} else {
  console.error(`💥 Found ${errors} syntax errors.`);
  process.exit(1);
}
