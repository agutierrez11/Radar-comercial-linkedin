const fs = require('fs');
const vm = require('vm');

const content = fs.readFileSync('staging.html', 'utf8');
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let blockIndex = 0;

while ((match = scriptRegex.exec(content)) !== null) {
  blockIndex++;
  const code = match[1];
  const tag = match[0].split('>')[0];
  if (tag.includes('src=')) continue; // skip external script tags
  
  const linesBefore = content.substring(0, match.index).split('\n').length;
  try {
    new vm.Script(code, { filename: 'staging.html', lineOffset: linesBefore - 1 });
    console.log(`Block ${blockIndex} (line ${linesBefore}): OK`);
  } catch (err) {
    console.error(`Block ${blockIndex} (line ${linesBefore}) ERROR: ${err.message}`);
    console.error(err.stack.split('\n').slice(0, 3).join('\n'));
  }
}
