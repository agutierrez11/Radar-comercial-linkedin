import re

def fix_active_class(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Make sure navigate(sec) adds active class to target section
    old_code = "const targetSec = document.getElementById('sec-' + sec);\n  if (targetSec) targetSec.classList.add('active');"
    new_code = """const targetSec = document.getElementById('sec-' + sec);
  if (targetSec) {
    targetSec.classList.add('active');
    targetSec.style.display = 'block';
  }"""

    content = content.replace(old_code, new_code)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_active_class(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_active_class(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Target section display block applied!")
