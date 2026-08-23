const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
const blocks = [...html.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi)];
for (let i = 0; i < blocks.length; i += 1) {
  new vm.Script(blocks[i][1], { filename: `index.html:inline-script-${i + 1}` });
}
console.log(`Inline script syntax passed: ${blocks.length} blocks`);
