import re

def fix_navigate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_nav = "document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));"
    new_nav = "document.querySelectorAll('.section').forEach(s => { s.classList.remove('active'); s.style.display = 'none'; });"

    if old_nav in content:
        content = content.replace(old_nav, new_nav)
        print(f"Fixed navigate() display hide logic in {filepath}")
    else:
        print(f"Pattern not found in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_navigate('index.html')
fix_navigate('staging.html')
