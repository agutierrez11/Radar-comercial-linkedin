import re

def unlock_all(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define unlockAnalyticsUI function cleanly
    unlock_func = """
function unlockAnalyticsUI() {
  const locked = document.getElementById('analytics-locked');
  const dashboard = document.getElementById('analytics-dashboard');
  if (locked) locked.style.display = 'none';
  if (dashboard) dashboard.style.display = 'block';
  if (typeof renderAnalytics === 'function') renderAnalytics();
}
window.unlockAnalyticsUI = unlockAnalyticsUI;
"""

    if 'function unlockAnalyticsUI()' not in content:
        content = content.replace("<script>", "<script>\n" + unlock_func, 1)

    # Make sure finalize() calls unlockAnalyticsUI()
    if 'unlockAnalyticsUI();' not in content:
        content = content.replace("function finalize() {", "function finalize() {\n  unlockAnalyticsUI();")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

unlock_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
unlock_all(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("unlockAnalyticsUI added to finalize and initializers!")
