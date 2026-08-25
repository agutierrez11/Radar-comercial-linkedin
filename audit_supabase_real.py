import os, requests, json

env_file = '.env'
env_url = None
env_key = None
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('SUPABASE_URL='):
                env_url = line.split('=', 1)[1].strip().strip('"')
            if line.startswith('SUPABASE_KEY=') or line.startswith('SUPABASE_ANON_KEY='):
                env_key = line.split('=', 1)[1].strip().strip('"')

print(f"ENV SUPABASE_URL: {env_url}")

# Check index.html keys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
supa_url_m = re.search(r"SUPA_URL\s*=\s*'([^']+)'", html)
supa_key_m = re.search(r"SUPA_KEY\s*=\s*'([^']+)'", html)

html_url = supa_url_m.group(1) if supa_url_m else None
html_key = supa_key_m.group(1) if supa_key_m else None

print(f"HTML SUPA_URL: {html_url}")
print(f"HTML SUPA_KEY (prefix): {html_key[:20]}..." if html_key else "HTML SUPA_KEY: None")

# Check table endpoints on html_url
tables = ['contacts', 'connections', 'user_vault_contacts', 'user_zip_files', 'contact_decisions', 'snapshots', 'messages']

print("\n--- Auditing HTML Supabase URL (yzpqclsfpktmsvjczroq) ---")
headers = {'apikey': html_key, 'Authorization': f'Bearer {html_key}'}
for t in tables:
    try:
        r = requests.get(f"{html_url}/rest/v1/{t}?select=*&limit=1", headers=headers, timeout=5)
        print(f"Table '{t}': HTTP {r.status_code} | Body: {r.text[:120]}")
    except Exception as e:
        print(f"Table '{t}': Error {e}")

print("\n--- Auditing ENV Supabase URL (hsrseeqhdtogpdqbveay) ---")
if env_url and env_key:
    headers_env = {'apikey': env_key, 'Authorization': f'Bearer {env_key}'}
    for t in tables:
        try:
            r = requests.get(f"{env_url}/rest/v1/{t}?select=*&limit=1", headers=headers_env, timeout=5)
            print(f"Table '{t}': HTTP {r.status_code} | Body: {r.text[:120]}")
        except Exception as e:
            print(f"Table '{t}': Error {e}")
