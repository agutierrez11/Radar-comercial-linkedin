import re

def remove_demo_load(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target_code = """document.addEventListener('DOMContentLoaded', () => {
  // Carga automática de los datos enriquecidos y navega directo a Mi Red
  if (typeof loadDemoData === 'function') {
    loadDemoData(true);
  }
});"""

    if target_code in content:
        content = content.replace(target_code, "// Automatic demo load removed on DOMContentLoaded")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed automatic demo load from {filepath}")
    else:
        print(f"Target code not found in {filepath}, searching pattern...")
        pattern = r"document\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*\{\s*//\s*Carga automática[\s\S]*?\}\);"
        new_content, count = re.subn(pattern, "// Automatic demo load removed", content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed automatic demo load pattern ({count} matches) from {filepath}")
        else:
            print(f"No pattern match found in {filepath}")

remove_demo_load(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
remove_demo_load(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
