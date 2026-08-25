def fix_quick_login(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace literal newline inside the string
    content = content.replace("prompt('🔒 Bóveda Privada del Administrador (Antonio).\nIngresa", r"prompt('🔒 Bóveda Privada del Administrador (Antonio). \n Ingresa")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_quick_login(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_quick_login(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Quick login literal newline fixed!")
