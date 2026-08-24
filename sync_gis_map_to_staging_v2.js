const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');
const stagingHtml = fs.readFileSync('staging.html', 'utf8');

const gisStart = indexHtml.indexOf('function initGisMap(contacts) {');
const headerStart = indexHtml.indexOf('function renderHeader() {', gisStart);

if (gisStart === -1 || headerStart === -1) {
  console.error('Failed to extract initGisMap from index.html');
  process.exit(1);
}

const cleanGisCode = indexHtml.substring(gisStart, headerStart);

const stGisStart = stagingHtml.indexOf('function initGisMap(contacts) {');
const stHeaderStart = stagingHtml.indexOf('function renderHeader() {', stGisStart);

if (stGisStart === -1 || stHeaderStart === -1) {
  console.error('Failed to find initGisMap bounds in staging.html');
  process.exit(1);
}

const newStaging = stagingHtml.substring(0, stGisStart) + cleanGisCode + stagingHtml.substring(stHeaderStart);
fs.writeFileSync('staging.html', newStaging, 'utf8');
console.log('✅ Successfully replaced initGisMap in staging.html with clean version from index.html');
