import re

def patch_navigate_unlock(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Modify navigate function to unlock analytics when navigating to analytics
    old_nav = "function navigate(secId) {"
    new_nav = """function navigate(secId) {
  if (secId === 'analytics') {
    const locked = document.getElementById('analytics-locked');
    const dashboard = document.getElementById('analytics-dashboard');
    if (locked) locked.style.display = 'none';
    if (dashboard) dashboard.style.display = 'block';
    if (typeof renderAnalytics === 'function') setTimeout(renderAnalytics, 50);
  }"""

    content = content.replace(old_nav, new_nav)

    # 2. Modify switchAnalyticsViewMode to ensure containers toggle correctly
    old_switch = "function switchAnalyticsViewMode(mode) {"
    new_switch = """function switchAnalyticsViewMode(mode) {
  const containerA = document.getElementById('analytics-view-container-a');
  const containerB = document.getElementById('analytics-view-container-b');
  const btnA = document.getElementById('ana-mode-btn-a');
  const btnB = document.getElementById('ana-mode-btn-b');
  
  const locked = document.getElementById('analytics-locked');
  const dashboard = document.getElementById('analytics-dashboard');
  if (locked) locked.style.display = 'none';
  if (dashboard) dashboard.style.display = 'block';

  if (mode === 'B') {
    if (containerA) containerA.style.display = 'none';
    if (containerB) containerB.style.display = 'block';
    if (btnA) { btnA.style.background = 'transparent'; btnA.style.borderColor = 'var(--border)'; }
    if (btnB) { btnB.style.background = 'var(--primary)'; btnB.style.color = '#ffffff'; btnB.style.borderColor = 'var(--primary)'; }
    if (typeof renderPowerBiEcharts === 'function') {
      setTimeout(renderPowerBiEcharts, 100);
    }
  } else {
    if (containerA) containerA.style.display = 'block';
    if (containerB) containerB.style.display = 'none';
    if (btnB) { btnB.style.background = 'transparent'; btnB.style.borderColor = 'var(--border)'; }
    if (btnA) { btnA.style.background = 'var(--primary)'; btnA.style.color = '#ffffff'; btnA.style.borderColor = 'var(--primary)'; }
    if (typeof renderAnalytics === 'function') setTimeout(renderAnalytics, 50);
  }
}"""

    pattern_switch = r'function switchAnalyticsViewMode\(mode\)\s*\{[\s\S]*?\n\}'
    content = re.sub(pattern_switch, new_switch, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_navigate_unlock(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
patch_navigate_unlock(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("auto_unlock_on_navigate applied!")
