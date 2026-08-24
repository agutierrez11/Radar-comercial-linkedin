const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');
const stagingHtml = fs.readFileSync('staging.html', 'utf8');

const navStartIdx = indexHtml.indexOf('function navigate(sec) {');
const navEndIdx = indexHtml.indexOf('// ═══════════════════════════════════════════════════════════════════════\n// PROFILE CARD', navStartIdx);

const cleanNavCode = indexHtml.substring(navStartIdx, navEndIdx);

const stNavStart = stagingHtml.indexOf('function navigate(sec) {');
const stNavEnd = stagingHtml.indexOf('// ═══════════════════════════════════════════════════════════════════════\n// PROFILE CARD', stNavStart);

if (stNavStart === -1 || stNavEnd === -1) {
  console.error('Failed to find navigate bounds in staging.html');
  process.exit(1);
}

const newStaging = stagingHtml.substring(0, stNavStart) + cleanNavCode + stagingHtml.substring(stNavEnd);
fs.writeFileSync('staging.html', newStaging, 'utf8');
console.log('✅ Replaced navigate & renderHeader in staging.html with clean version from index.html');
