import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="welcome-gateway-modal"')
if idx != -1:
    print(content[idx:idx+1500])
else:
    print("welcome-gateway-modal not found")
