import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

main_open_line = 0
main_close_line = 0

for i, line in enumerate(lines, start=1):
    if '<main' in line:
        print(f"Line {i}: {line.strip()[:100]}")
    if '</main>' in line:
        print(f"Line {i}: {line.strip()[:100]}")
    if 'id="sec-' in line:
        print(f"Line {i}: {line.strip()[:100]}")
