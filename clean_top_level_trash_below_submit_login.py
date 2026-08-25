import re

def clean_trash(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find window.submitCustomLogin = submitCustomLogin; and remove any trailing unclosed code until next valid function or section
    pattern = r'window\.submitCustomLogin = submitCustomLogin;\s*const usernameInput = document\.getElementById\(\'login-username-input\'\);[\s\S]*?(?=// ═|function |window\.|document\.addEventListener)'
    
    if re.search(pattern, content):
        content = re.sub(pattern, "window.submitCustomLogin = submitCustomLogin;\n\n", content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned trailing trash below submitCustomLogin in {filepath}")
    else:
        print(f"No trailing trash pattern match in {filepath}")

clean_trash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
clean_trash(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
