import re

def fix_navigate_binding(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove invalid prepended window.navigate = navigate
    content = content.replace("window.navigate = navigate;\nfunction navigate(sec)", "function navigate(sec)")
    content = content.replace("window.loadDemoData = loadDemoData;\nasync function loadDemoData(", "async function loadDemoData(")

    # Add bindings after function definitions
    old_nav_end = "  if (sec === 'analytics') {"
    new_nav_end = "window.navigate = navigate;\n  if (sec === 'analytics') {"

    content = content.replace(old_nav_end, new_nav_end)

    if "window.loadDemoData = loadDemoData;" not in content:
        content = content.replace("finalize();\n    initGisMap(S.contacts);", "finalize();\n    initGisMap(S.contacts);\n    window.loadDemoData = loadDemoData;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_navigate_binding(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_navigate_binding(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Fix navigate binding applied!")
