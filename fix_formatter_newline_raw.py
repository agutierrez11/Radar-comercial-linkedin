def fix_raw(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace literal newline inside the string
    content = content.replace("formatter: '{b}\n{c} contactos',", r"formatter: '{b} \n {c} contactos',")
    content = content.replace("formatter: '{b}\r\n{c} contactos',", r"formatter: '{b} \n {c} contactos',")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_raw(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_raw(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Raw string literal newline fix applied!")
