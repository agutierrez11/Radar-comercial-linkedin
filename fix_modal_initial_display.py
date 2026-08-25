import re

def fix_modal_display(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('<div class="modal-overlay" id="login-modal">', '<div class="modal-overlay open" id="login-modal" style="display:flex !important; opacity:1 !important; pointer-events:auto !important; z-index:99999 !important;">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_modal_display(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_modal_display(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Login modal initial flex display fixed!")
