import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="sec-analytics"')
if idx != -1:
    print("--- HTML 500 CHARS BEFORE sec-analytics ---")
    print(content[idx-500:idx])
