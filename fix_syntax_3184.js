const fs = require('fs');

let content = fs.readFileSync('staging.html', 'utf8');

if (content.includes('}"if (sec === \'network\') {')) {
  content = content.replace('}"if (sec === \'network\') {', '}\n\n  if (sec === \'network\') {');
  fs.writeFileSync('staging.html', content, 'utf8');
  console.log('✅ Fixed syntax error at line 3184 (}"if -> } if)');
} else {
  console.log('Target string not found on line 3184');
}
