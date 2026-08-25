import re

def fix_stray_divs(filepath):
    print(f"Fixing stray divs in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove stray line 1224-1225: <!-- ── PROFILE ── --> </div><!-- END sec-network -->
    stray_pattern = r'<!-- ── PROFILE ── -->\s*</div><!-- END sec-network -->\s*<div class="section" id="sec-profile">'
    replacement = '<!-- ── PROFILE ── -->\n    <div class="section" id="sec-profile">'
    
    if re.search(stray_pattern, content):
        content = re.sub(stray_pattern, replacement, content)
        print("Removed stray line before sec-profile!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_stray_divs('index.html')
fix_stray_divs('staging.html')
