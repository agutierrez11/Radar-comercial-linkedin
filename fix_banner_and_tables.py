import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix banner flex child min-width: 0
    content = content.replace(
        '<div style="display:flex; align-items:center; gap:12px; flex:1;">',
        '<div style="display:flex; align-items:center; gap:12px; flex:1; min-width:0;">'
    )
    
    # 2. Fix inner text container in banner min-width: 0
    content = content.replace(
        '<div>\n      <div style="display:flex; align-items:center; gap:8px;">',
        '<div style="min-width:0; flex:1;">\n      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched flex min-width on {filepath}")

patch_file('index.html')
patch_file('staging.html')
