import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('S.loadedParts')
while idx != -1:
    print(content[idx-50:idx+150])
    print("---")
    idx = content.find('S.loadedParts', idx+150)
