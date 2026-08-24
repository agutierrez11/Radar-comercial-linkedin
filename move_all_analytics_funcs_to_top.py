import re

def move_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    top_funcs = """
window.switchAnalyticsViewMode = function(mode) {
  window.currentAnalyticsViewMode = mode;
  const btnA = document.getElementById('ana-mode-btn-a');
  const btnB = document.getElementById('ana-mode-btn-b');
  const containerA = document.getElementById('analytics-view-container-a');
  const containerB = document.getElementById('analytics-view-container-b');

  if (mode === 'B') {
    if (btnB) { btnB.classList.add('active'); btnB.style.background = 'var(--accent)'; btnB.style.color = '#fff'; }
    if (btnA) { btnA.classList.remove('active'); btnA.style.background = 'transparent'; btnA.style.color = 'var(--text-muted)'; }
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    if (typeof renderPowerBiEcharts === 'function') renderPowerBiEcharts();
    if (typeof showToast === 'function') showToast('⚡ Vista Power BI Executive Suite (Apache ECharts) activada.', '⚡');
  } else {
    if (btnA) { btnA.classList.add('active'); btnA.style.background = 'var(--accent)'; btnA.style.color = '#fff'; }
    if (btnB) { btnB.classList.remove('active'); btnB.style.background = 'transparent'; btnB.style.color = 'var(--text-muted)'; }
    if (containerB) containerB.style.display = 'none';
    if (containerA) containerA.style.display = 'block';
  }
};
var switchAnalyticsViewMode = window.switchAnalyticsViewMode;
"""

    if 'var switchAnalyticsViewMode = window.switchAnalyticsViewMode;' not in content:
        content = content.replace("<script>", "<script>\n" + top_funcs, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

move_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
move_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("All analytics functions elevated!")
