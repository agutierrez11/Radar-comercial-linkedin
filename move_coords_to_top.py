import re

def fix_coords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change const CITY_COORDS and const COUNTRY_COORDS to var
    content = content.replace("const COUNTRY_COORDS =", "var COUNTRY_COORDS =")
    content = content.replace("const CITY_COORDS =", "var CITY_COORDS =")

    # Declare var COUNTRY_COORDS, CITY_COORDS at top if missing
    top_vars = "var COUNTRY_COORDS = window.COUNTRY_COORDS || {};\nvar CITY_COORDS = window.CITY_COORDS || {};\n"
    if 'var COUNTRY_COORDS = window.COUNTRY_COORDS' not in content:
        content = content.replace("<script>", "<script>\n" + top_vars, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_coords(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_coords(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
