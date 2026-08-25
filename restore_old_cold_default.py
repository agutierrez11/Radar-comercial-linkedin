import re

def restore_old_cold(filepath):
    print(f"Restoring old_cold criteria to on: true in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update S.criteria array definition: old_cold on: true
    content = content.replace("id: 'old_cold',\n      label: 'Conexión >4 años, sin DMs y sin valor estratégico',\n      on: false,", "id: 'old_cold',\n      label: 'Conexión >4 años, sin DMs y sin valor estratégico',\n      on: true,")
    content = content.replace("id: 'old_cold',\r\n      label: 'Conexión >4 años, sin DMs y sin valor estratégico',\r\n      on: false,", "id: 'old_cold',\r\n      label: 'Conexión >4 años, sin DMs y sin valor estratégico',\r\n      on: true,")

    # 2. Update restoreLocalVault sanitization so it doesn't force old_cold to false
    content = content.replace("if (cr.id === 'old_cold' || cr.id === 'no_country') cr.on = false;", "if (cr.id === 'no_country') cr.on = false;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully restored old_cold in {filepath}")

restore_old_cold('index.html')
restore_old_cold('staging.html')
