import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('temp_script7.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(5810, 5840):
    if i <= len(lines):
        print(f"Line {i}: {lines[i-1].rstrip()}")
