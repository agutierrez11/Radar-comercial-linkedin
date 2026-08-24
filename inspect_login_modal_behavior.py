import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="login-modal"')
if idx != -1:
    print(content[idx:idx+1200])

idx2 = content.find('function closeLoginModal')
if idx2 != -1:
    print("--- CLOSE LOGIN MODAL ---")
    print(content[idx2:idx2+600])

idx3 = content.find('function switchSessionVault')
if idx3 != -1:
    print("--- SWITCH SESSION VAULT ---")
    print(content[idx3:idx3+800])
