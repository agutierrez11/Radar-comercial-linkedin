import re
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
combined_js = "\n;\n".join(scripts)

with open('temp_check.js', 'w', encoding='utf-8') as f:
    f.write(combined_js)

res = subprocess.run(['node', '--check', 'temp_check.js'], capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: JAVASCRIPT SYNTAX IS 100% VALID! NO ERRORS FOUND.")
else:
    print("ERROR: JS SYNTAX ERROR DETECTED:")
    print(res.stderr)
