import re

def fix_placement(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean top assignment
    content = content.replace("window.submitCustomLogin = submitCustomLogin;\nfunction submitCustomLogin(", "function submitCustomLogin(")
    content = content.replace("window.submitCustomLogin = submitCustomLogin;\nasync function loadDemoData(", "async function loadDemoData(")

    # Place window.submitCustomLogin = submitCustomLogin AFTER the function block
    pattern = r'(function submitCustomLogin\(targetUser\)\s*\{[\s\S]*?\n\})'
    replacement = r'\1\nwindow.submitCustomLogin = submitCustomLogin;'
    
    # Replace only if not already after
    if 'window.submitCustomLogin = submitCustomLogin;' not in content:
        content = re.sub(pattern, replacement, content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_placement(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_placement(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Window submitCustomLogin placement fixed!")
