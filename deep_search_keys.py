import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def search_for_key():
    base_dirs = [
        r"C:\Users\Antonio\.gemini\antigravity-ide\brain",
        r"C:\Users\Antonio\.gemini\antigravity-ide\scratch",
        r"C:\Users\Antonio\.gemini\config",
        r"C:\Users\Antonio\.gemini",
        r"C:\Users\Antonio\AppData\Roaming",
        r"C:\Users\Antonio\Desktop"
    ]

    found_keys = set()

    for base in base_dirs:
        if not os.path.exists(base):
            continue
        print(f"Buscando en: {base}...")
        for root, dirs, files in os.walk(base):
            # Skip node_modules or large git objects to speed up
            if 'node_modules' in root or '.git' in root:
                continue
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        if 'nvapi-' in content:
                            idx = 0
                            while True:
                                idx = content.find('nvapi-', idx)
                                if idx == -1:
                                    break
                                # Extract full key (starts with nvapi- and usually 64 chars)
                                raw = content[idx:idx+75]
                                key_candidate = raw.split()[0].split('"')[0].split("'")[0].split('\n')[0].split('\\')[0].strip()
                                if len(key_candidate) >= 20:
                                    found_keys.add((filepath, key_candidate))
                                idx += 6
                except Exception:
                    pass

    print("\n==========================================")
    print(f"RESULTADO: {len(found_keys)} claves nvapi- encontradas")
    print("==========================================")
    for path, key in found_keys:
        print(f"Archivo: {path}")
        print(f"Clave: {key}")

if __name__ == "__main__":
    search_for_key()
