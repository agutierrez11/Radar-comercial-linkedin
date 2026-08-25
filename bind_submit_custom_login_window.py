import re

def bind_submit_custom(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'window.submitCustomLogin = submitCustomLogin;' not in content:
        content = content.replace("function submitCustomLogin(targetUser) {", "window.submitCustomLogin = submitCustomLogin;\nfunction submitCustomLogin(targetUser) {")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

bind_submit_custom(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
bind_submit_custom(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("window.submitCustomLogin bound successfully!")
