"""switch_key.py - Cambia anon key por service role en index.html"""

import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

secret_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
old_key = "var SUPA_KEY = 'sb_publishable_CeImc3_1L9K7bOTvIBKxvQ_yLRRfYmi';"
new_key = f"var SUPA_KEY = '{secret_key}'; // Service Role - solo uso local BYOD"

if old_key in content:
    content = content.replace(old_key, new_key, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] Service role key configurada para acceso local BYOD')
else:
    idx = content.find('sb_publishable_CeImc3')
    if idx > 0:
        print('Key en pos:', idx)
        print('Contexto:', repr(content[idx-30:idx+80]))
    else:
        print('No encontrada la key en el HTML')
