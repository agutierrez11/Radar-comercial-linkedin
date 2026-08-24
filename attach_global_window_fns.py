import re

def attach_globals(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure loadDemoData, navigate, renderAnalytics are globally attached
    attachments = """
window.loadDemoData = typeof loadDemoData !== 'undefined' ? loadDemoData : window.loadDemoData;
window.navigate = typeof navigate !== 'undefined' ? navigate : window.navigate;
window.renderAnalytics = typeof renderAnalytics !== 'undefined' ? renderAnalytics : window.renderAnalytics;
"""

    if 'window.loadDemoData = loadDemoData' not in content:
        content = content.replace("async function loadDemoData(", "window.loadDemoData = loadDemoData;\nasync function loadDemoData(")
        content = content.replace("function navigate(", "window.navigate = navigate;\nfunction navigate(")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

attach_globals(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
attach_globals(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Globals attached!")
