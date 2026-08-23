const assert = require('node:assert/strict');
global.window = {};
require('./radar_core.js');
const { parseQuery, searchVault } = window.RadarCore;

const contacts = [
  { id: 1, name: 'María Test', company: 'Hospital Demo', position: 'Compras', country: 'México', url: 'https://linkedin.com/in/maria-test', msg_count: 2 },
  { id: 2, name: 'Pedro Test', company: 'Fintech Demo', position: 'CEO', country: 'Colombia', url: 'https://linkedin.com/in/pedro-test', msg_count: 1, last_msg_snippet: 'Hablemos de pagos y gateway' }
];

const messages = [
  { 'CONVERSATION ID': 'c1', FROM: 'Antonio Gutiérrez', TO: 'María Test', DATE: '2020-05-10 10:00:00', CONTENT: 'Te ofrezco batas quirúrgicas y cubrebocas para hospitales.' },
  { 'CONVERSATION ID': 'c1', FROM: 'María Test', TO: 'Antonio Gutiérrez', DATE: '2020-05-11 10:00:00', CONTENT: 'Sí, envíame precio y disponibilidad.' },
  { 'CONVERSATION ID': 'c2', FROM: 'Pedro Test', TO: 'Antonio Gutiérrez', DATE: '2024-01-01 10:00:00', CONTENT: '¿Te interesa una solución de pagos?' }
];

const parsed = parseQuery('yo ofrecí batas 2020');
assert.equal(parsed.direction, 'sent');
assert.deepEqual(parsed.years, [2020]);
assert.ok(parsed.terms.includes('bata'));

const result = searchVault({ query: 'yo ofrecí batas 2020', contacts, messages, ownerName: 'Antonio Gutiérrez' });
assert.equal(result.hasFullMessages, true);
assert.equal(result.counts.conversations, 1);
assert.equal(result.results[0].type, 'conversation');
assert.equal(result.results[0].commercialDirection, 'bidireccional');
assert.ok(result.results[0].reason.includes('batas'));

const curated = searchVault({ query: 'pagos', contacts, messages: [], ownerName: 'Antonio Gutiérrez' });
assert.equal(curated.hasFullMessages, false);
assert.equal(curated.counts.contacts, 1);
assert.equal(curated.results[0].participant, 'Pedro Test');

console.log('RadarCore tests passed');
