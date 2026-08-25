import re

def patch_login_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = "if (typeof renderNetworkTable === 'function') renderNetworkTable();"
    replacement = "if (typeof renderNetworkTable === 'function') renderNetworkTable();\n      if (typeof navigate === 'function') navigate('network');"

    if target in content and "navigate('network');" not in content[content.find(target):content.find(target)+200]:
        content = content.replace(target, replacement, 1)
        print(f"Patched master login navigation in {filepath}")
    else:
        print(f"Already patched or target not found in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_login_nav('index.html')
patch_login_nav('staging.html')
