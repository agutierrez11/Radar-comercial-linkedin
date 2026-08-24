import re
import sys

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content, re.IGNORECASE)
    print(f"File: {filepath} ({len(scripts)} scripts)")
    
    for idx, s in enumerate(scripts):
        # Find stray html tag closures inside script
        lines = s.split('\n')
        for l_num, line in enumerate(lines, 1):
            if '</div>' in line or '</section>' in line or '</form>' in line or '</div><!--' in line:
                if not ('//' in line or '/*' in line or '`' in line or '"' in line or "'" in line):
                    print(f"  [ERROR] Script #{idx+1} line {l_num} has stray HTML tag: {line.strip()}")

check_file('index.html')
check_file('staging.html')
