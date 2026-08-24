const fs = require('fs');

const indexHtml = fs.readFileSync('index.html', 'utf8');
const stagingHtml = fs.readFileSync('staging.html', 'utf8');

const navStartIdx = indexHtml.indexOf('function navigate(sec) {');
const profileStartIdx = indexHtml.indexOf('function renderProfile()', navStartIdx);

if (navStartIdx === -1 || profileStartIdx === -1) {
  console.error('Failed to extract navigate & renderHeader from index.html');
  process.exit(1);
}

const cleanCode = indexHtml.substring(navStartIdx, profileStartIdx);

const stNavStart = stagingHtml.indexOf('function navigate(sec) {');
const stProfileStart = stagingHtml.indexOf('function renderProfile()', stNavStart);

if (stNavStart === -1 || stProfileStart === -1) {
  console.error('Failed to find bounds in staging.html');
  process.exit(1);
}

const newStaging = stagingHtml.substring(0, stNavStart) + cleanCode + stagingHtml.substring(stProfileStart);
fs.writeFileSync('staging.html', newStaging, 'utf8');
console.log('✅ Successfully synced navigate & renderHeader in staging.html from index.html');
