import re

def bind_S(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'window.S = S;' not in content:
        content = content.replace("const S = {", "const S = window.S = {")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

bind_S(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
bind_S(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("window.S bound successfully!")
