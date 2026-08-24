import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('REQUIRES_ZIP')
while idx != -1:
    print(content[idx:idx+200])
    idx = content.find('REQUIRES_ZIP', idx+200)
