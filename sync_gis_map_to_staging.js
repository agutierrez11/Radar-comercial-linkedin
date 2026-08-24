const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');
const stagingHtml = fs.readFileSync('staging.html', 'utf8');

// Extract clean initGisMap from indexHtml
const gisStart = indexHtml.indexOf('function initGisMap(contacts) {');
const gisEnd = indexHtml.indexOf('// ═══════════════════════════════════════════════════════════════════════\n// HEADER KPIs', gisStart);

if (gisStart === -1 || gisEnd === -1) {
  console.error('Failed to extract initGisMap from index.html');
  process.exit(1);
}

const cleanGisCode = indexHtml.substring(gisStart, gisEnd);

// Replace in stagingHtml
const stGisStart = stagingHtml.indexOf('function initGisMap(contacts) {');
const stGisEnd = stagingHtml.indexOf('// ═══════════════════════════════════════════════════════════════════════\n// HEADER KPIs', stGisStart);

if (stGisStart === -1 || stGisEnd === -1) {
  console.error('Failed to find initGisMap bounds in staging.html');
  process.exit(1);
}

const newStaging = stagingHtml.substring(0, stGisStart) + cleanGisCode + stagingHtml.substring(stGisEnd);
fs.writeFileSync('staging.html', newStaging, 'utf8');
console.log('✅ Replaced initGisMap in staging.html with clean version from index.html');
