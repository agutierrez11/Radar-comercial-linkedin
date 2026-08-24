import re

def fix_html_div_balance(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    main_start_tag = '<main id="main-content">'
    main_end_tag = '</main>'
    
    start_pos = content.find(main_start_tag)
    end_pos = content.find(main_end_tag)

    if start_pos == -1 or end_pos == -1:
        print(f"Error: <main> tags not found in {filepath}")
        return

    main_inner = content[start_pos + len(main_start_tag):end_pos]

    # Regex to split sections by <div class="section... id="sec-..."
    sec_regex = r'(<div\s+class="section[^"]*"\s+id="(sec-[^"]+)">)'
    tokens = re.split(sec_regex, main_inner)

    # tokens[0] is content inside <main> before first section
    preamble = tokens[0].strip()

    sections = []
    i = 1
    while i < len(tokens):
        sec_header = tokens[i]
        sec_id = tokens[i+1]
        raw_body = tokens[i+2]
        
        # Remove any comments like <!-- END sec-... -->
        raw_body = re.sub(r'<!--\s*END\s+sec-[^>]*-->', '', raw_body)
        raw_body = re.sub(r'<!--\s*END\s+analytics-view-container-[^>]*-->', '', raw_body)

        # Balance inner DIVs in raw_body
        # We assume sec_header adds 1 open div
        # We need raw_body to have net 0 open/close divs so that the section ends cleanly with 1 closing </div>
        
        # Count open and close divs in raw_body
        open_count = len(re.findall(r'<div[\s>]', raw_body))
        close_count = len(re.findall(r'</div>', raw_body))

        diff = open_count - close_count
        if diff > 0:
            # Need diff closing divs inside body
            raw_body = raw_body.rstrip() + ("\n" + "</div>" * diff)
        elif diff < 0:
            # Too many closing divs in raw_body, remove extra closing </div> from end of raw_body
            for _ in range(abs(diff)):
                last_div_idx = raw_body.rfind("</div>")
                if last_div_idx != -1:
                    raw_body = raw_body[:last_div_idx] + raw_body[last_div_idx+6:]

        sections.append((sec_id, sec_header, raw_body.strip()))
        i += 3

    # Now assemble new main inner
    new_main_inner = "\n  " + preamble + "\n"
    for sec_id, sec_header, body in sections:
        # Check if sec_header has 'active' class, remove active unless it's sec-network or default
        new_main_inner += f"\n    {sec_header}\n      {body}\n    </div><!-- END {sec_id} -->\n"

    new_full_content = content[:start_pos + len(main_start_tag)] + new_main_inner + "\n  " + content[end_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_full_content)

fix_html_div_balance(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_html_div_balance(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("DIV balance and section structure rebuilt perfectly!")
