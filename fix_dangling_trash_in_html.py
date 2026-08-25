import re

def fix_dangling(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: window.submitCustomLogin = submitCustomLogin; followed by dangling statements until next comment section header
    pattern = r'window\.submitCustomLogin = submitCustomLogin;\s*window\.currentAuthUser[\s\S]*?(?=// ═|function |window\.switchVaultViewMode)'
    
    if re.search(pattern, content):
        content = re.sub(pattern, "window.submitCustomLogin = submitCustomLogin;\n\n", content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Dangling trash removed from {filepath}")
    else:
        print(f"Dangling trash pattern not found in {filepath}")

fix_dangling(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_dangling(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
