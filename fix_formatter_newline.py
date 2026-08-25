def fix_formatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    bad_str = "formatter: '{b}\n{c} contactos',"
    good_str = "formatter: '{b}\\n{c} contactos',"

    if bad_str in content:
        content = content.replace(bad_str, good_str)
        print(f"Fixed bad newline in {filepath}")
    else:
        print(f"bad_str not found in {filepath}, checking alternate patterns...")
        content = content.replace("formatter: '{b}\n{c}", "formatter: '{b}\\n{c}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_formatter(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_formatter(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
