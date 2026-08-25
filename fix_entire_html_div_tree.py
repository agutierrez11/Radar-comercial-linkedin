import re

def fix_html_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Check for duplicate id="sec-network"
    sec_net_matches = list(re.finditer(r'<div\s+class="section[^"]*"\s+id="sec-network">', content))
    print(f"Found {len(sec_net_matches)} occurrences of sec-network")

    if len(sec_net_matches) > 1:
        # We need to remove the first duplicate block (which was inserted prematurely around line 1219)
        # Let's inspect where the first sec-network starts and where the second sec-network starts
        pos1 = sec_net_matches[0].start()
        pos2 = sec_net_matches[1].start()
        
        # Find where sec-network 1 ends (before <div class="section" id="sec-profile"> or similar)
        # In our inspection: line 1412 is sec-profile, line 1466 is sec-network 2.
        # Wait, let's remove the duplicated block between line 1219 and line 1412!
        sec_prof_match = re.search(r'<!-- ── PROFILE ── -->\s*</div><!-- END sec-[^>]+-->\s*<div\s+class="section"\s+id="sec-profile">', content)
        if sec_prof_match:
            end_dup = sec_prof_match.start()
            print(f"Removing duplicate sec-network block from char {pos1} to {end_dup}")
            content = content[:pos1] + content[end_dup:]

    # 2. Fix old_cold criterion in S.criteria: change on: true to on: false for old_cold
    # Search for id: 'old_cold' block
    old_cold_pattern = r"(id:\s*'old_cold',\s*label:\s*'Conexión >4 años, sin DMs y sin valor estratégico',\s*)on:\s*true"
    if re.search(old_cold_pattern, content):
        content = re.sub(old_cold_pattern, r"\1on: false", content)
        print("Updated old_cold criterion default to on: false")

    # 3. Ensure contacts-table has class="compact-table" if present
    content = content.replace('<table id="contacts-table">', '<table id="contacts-table" class="compact-table">')

    # 4. Fix banner padding / text truncation on top banners (#ronan-ab-banner, #matraix-monthly-reminder-banner, etc.)
    # Ensure all top banners have overflow: hidden, padding: 12px 16px, box-sizing: border-box, max-width: 100%
    content = content.replace('id="ronan-ab-banner" style="display:none; background:linear-gradient', 'id="ronan-ab-banner" style="display:none; width:100%; box-sizing:border-box; overflow:hidden; background:linear-gradient')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved fixes to {filepath}")

fix_html_file('index.html')
if re.search(r'index\.html', 'staging.html'):
    try:
        fix_html_file('staging.html')
    except Exception as e:
        print("staging.html error:", e)
