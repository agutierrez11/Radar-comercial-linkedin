import re

target_numbers = ['2953', '3039', '447', '541', '296', '271', '2087', '25110']

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

findings = []

for idx, line in enumerate(lines, 1):
    for num in target_numbers:
        if num in line:
            classification = 'documentación o comentario'
            if '//' in line or '<!--' in line or '/*' in line:
                classification = 'documentación o comentario'
            elif 'slice(0,' in line:
                classification = 'hardcode indebido'
            elif 'showToast' in line or 'console.log' in line or 'alert' in line:
                classification = 'documentación o comentario'
            elif 'const ' in line or 'let ' in line or 'var ' in line:
                classification = 'dato real de fixture'
            elif '<div' in line or '<span' in line or '<p' in line:
                classification = 'contador derivado'

            findings.append({
                'line': idx,
                'number': num,
                'content': line.strip(),
                'classification': classification
            })

print(f"[AUDIT] Found {len(findings)} references to target numbers.")
for f in findings:
    print(f"Line {f['line']}: [{f['number']}] ({f['classification']}) -> {f['content'][:80]}")
