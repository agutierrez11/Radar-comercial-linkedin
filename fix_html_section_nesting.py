import re

def fix_section_nesting(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <main id="main-content"> and </main>
    main_start = content.find('<main id="main-content">')
    main_end = content.find('</main>')
    
    if main_start == -1 or main_end == -1:
        print("Main bounds not found!")
        return

    main_inner = content[main_start + len('<main id="main-content">'):main_end]

    # Split main_inner by <div class="section" id="...
    section_pattern = r'(<div class="section"[^>]*id=["\'](sec-[^"\']+)["\'][^>]*>)'
    parts = re.split(section_pattern, main_inner)
    
    # Reconstruct clean sections where each section is self-contained and closed
    cleaned_sections = []
    
    # parts[0] is preamble before first section
    preamble = parts[0].strip()
    
    i = 1
    sections_map = {}
    while i < len(parts):
        sec_header = parts[i]
        sec_id = parts[i+1]
        sec_body = parts[i+2]
        
        # Remove trailing </div> if present in body to clean nesting
        # Strip outer trailing closing divs
        body_clean = sec_body.strip()
        
        # Save to map (keep first if duplicate)
        if sec_id not in sections_map:
            sections_map[sec_id] = (sec_header, body_clean)
        
        i += 3

    # Now rebuild main inner cleanly
    new_main_content = "\n" + preamble + "\n"
    for sec_id, (header, body) in sections_map.items():
        # Ensure body ends with a closing </div> for the section
        # Count <div> vs </div> in body
        open_divs = len(re.findall(r'<div[\s>]', body)) + 1 # +1 for section div header
        close_divs = len(re.findall(r'</div>', body))
        
        needed_closes = open_divs - close_divs
        if needed_closes > 0:
            body += ("\n" + "</div>" * needed_closes)
        elif needed_closes < 0:
            # Too many closing divs, trim extra </div> at the end
            for _ in range(abs(needed_closes)):
                if body.rstrip().endswith("</div>"):
                    body = body.rstrip()[:-6].strip()

        new_main_content += f"\n    {header}\n{body}\n    </div><!-- END {sec_id} -->\n"

    new_content = content[:main_start + len('<main id="main-content">')] + new_main_content + "\n  " + content[main_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_section_nesting(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_section_nesting(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Section nesting fixed!")
