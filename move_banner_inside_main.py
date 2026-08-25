import re

def move_banner(filepath):
    print(f"Moving banner inside #main-content in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the banner HTML block
    banner_match = re.search(r'(<!-- 🔔 BOT RECORDATORIO DE ACTUALIZACIÓN MENSUAL DE BÓVEDA.*?</div>\s*<!-- MODAL GUÍA SOLICITUD LINKEDIN ZIP -->)', content, re.DOTALL)
    if not banner_match:
        print("Banner match not found!")
        return

    banner_html = banner_match.group(1)
    
    # Remove banner from current location
    content = content.replace(banner_html, '')

    # Insert banner right after <main id="main-content">
    content = content.replace('<main id="main-content">', '<main id="main-content">\n\n  ' + banner_html)

    # Fix margin on banner to fit inside main-content: margin: 0 0 16px 0
    content = content.replace('margin:16px 24px 0 24px;', 'margin:0 0 16px 0; width:100%; box-sizing:border-box;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully moved banner inside #main-content in {filepath}")

move_banner('index.html')
move_banner('staging.html')
