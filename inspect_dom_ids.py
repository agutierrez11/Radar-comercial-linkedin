with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

def inspect_fn(name):
    m = re.search(r'function\s+' + name + r'\s*\([^)]*\)\s*\{[\s\S]*?\n\}', content)
    if m:
        code = m.group(0)
        # find all document.getElementById calls
        ids = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', code)
        print(f"=== {name} IDs ===")
        print(ids)
    else:
        print(f"=== {name} NOT FOUND ===")

inspect_fn('renderNetwork')
inspect_fn('renderGISMap')
inspect_fn('renderNetworkTable')
inspect_fn('applyNetworkFilters')
inspect_fn('switchVaultViewMode')
