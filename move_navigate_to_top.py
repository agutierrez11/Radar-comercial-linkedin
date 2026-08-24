import re

def move_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    top_nav = """
window.navigate = function(sec) {
  if (typeof REQUIRES_ZIP !== 'undefined' && REQUIRES_ZIP.includes(sec) && S.loadedParts && !S.loadedParts.connections) {
    alert("⚠️ Carga primero tu archivo de contactos (Connections.csv) para habilitar esta sección.");
    return;
  }
  if (typeof S !== 'undefined') S.activeSection = sec;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const targetSec = document.getElementById('sec-' + sec);
  if (targetSec) targetSec.classList.add('active');
  const targetNav = document.querySelector(`[data-section="${sec}"]`);
  if (targetNav) targetNav.classList.add('active');

  if (sec === 'network' && typeof gisMapInstance !== 'undefined' && gisMapInstance) {
    setTimeout(() => { if (gisMapInstance) gisMapInstance.invalidateSize(); }, 150);
  }
  if (sec === 'graph' && typeof renderCosmaGraph === 'function') {
    setTimeout(() => { renderCosmaGraph(); }, 100);
  }
  if (sec === 'crm') {
    const board = document.getElementById('crm-kanban-board');
    if (board) board.style.display = 'grid';
    requestAnimationFrame(() => { if (typeof renderCRM === 'function') renderCRM(); });
  }
  if (sec === 'analytics') {
    requestAnimationFrame(() => { if (typeof renderAnalytics === 'function') renderAnalytics(); });
  }
};
var navigate = window.navigate;
"""

    if 'var navigate = window.navigate;' not in content:
        content = content.replace("<script>", "<script>\n" + top_nav, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

move_nav(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
move_nav(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("window.navigate elevated to top!")
