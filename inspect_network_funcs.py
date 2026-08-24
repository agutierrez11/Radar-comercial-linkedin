with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

def print_fn(name):
    m = re.search(r'function\s+' + name + r'\s*\([^)]*\)\s*\{[\s\S]*?\n\}', content)
    if m:
        print(f"=== {name} ===")
        print(m.group(0)[:1500])
    else:
        print(f"=== {name} NOT FOUND ===")

print_fn('renderNetwork')
print_fn('renderGISMap')
print_fn('renderNetworkTable')
print_fn('switchVaultViewMode')
print_fn('navigate')
