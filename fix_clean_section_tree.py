import re

def fix_clean_sections(filepath):
    print(f"Cleaning sections in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Restore clean section boundaries
    # Let's inspect where sec-upload starts
    up_idx = content.find('<div class="section" id="sec-upload">')
    prof_idx = content.find('<div class="section" id="sec-profile">')
    net_idx = content.find('<div class="section" id="sec-network">')

    print(f"Indices: upload={up_idx}, profile={prof_idx}, network={net_idx}")

    # Make sure sec-upload is closed before sec-profile
    if prof_idx > up_idx:
        between_up_prof = content[up_idx:prof_idx]
        if between_up_prof.count('<div') != between_up_prof.count('</div>'):
            print("Fixing div balance between sec-upload and sec-profile")
            # Replace end of sec-upload before sec-profile
            content = re.sub(
                r'(\s*</div>\s*<!-- END sec-upload -->|\s*</div>\s*<!-- ── PROFILE ── -->)',
                '\n    </div><!-- END sec-upload -->\n\n    <!-- ── PROFILE ── -->\n',
                content
            )

    # Make sure sec-profile is closed before sec-network
    if net_idx > prof_idx:
        between_prof_net = content[prof_idx:net_idx]
        div_open = between_prof_net.count('<div')
        div_close = between_prof_net.count('</div>')
        print(f"Between profile and network: open={div_open}, close={div_close}")
        if div_open > div_close:
            needed_closes = "</div>" * (div_open - div_close)
            content = content[:net_idx] + needed_closes + "\n\n    " + content[net_idx:]
            print(f"Inserted {div_open - div_close} closing divs before sec-network")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Finished clean sections fix on {filepath}")

fix_clean_sections('index.html')
fix_clean_sections('staging.html')
