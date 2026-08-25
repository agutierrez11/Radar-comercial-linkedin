import re, sys

def validate_html(filepath):
    print(f"--- Validating {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    ids_to_check = ['sec-network', 'net-tbody', 'net-empty', 'contacts-table', 'net-kpis', 'ronan-ab-banner']
    for id_name in ids_to_check:
        matches = len(re.findall(rf'id="{id_name}"', content))
        status = "OK" if matches == 1 else f"ERROR ({matches} instances)"
        print(f"ID '{id_name}': {status}")

    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    print(f"Total script blocks: {len(scripts)}")

validate_html('index.html')
validate_html('staging.html')
