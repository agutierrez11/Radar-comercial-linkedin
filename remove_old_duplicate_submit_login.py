import re

def remove_old_dup(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find first submitCustomLogin function block around 5717
    pattern = r'function submitCustomLogin\(targetUser\)\s*\{[\s\S]*?window\.submitCustomLogin\s*=\s*submitCustomLogin;'
    matches = list(re.finditer(pattern, content))
    print(f"Found {len(matches)} submitCustomLogin blocks in {filepath}")

    if len(matches) > 1:
        # Keep only the last one (pristine) and remove the first broken one
        first_match = matches[0]
        content = content[:first_match.start()] + content[first_match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed old duplicate submitCustomLogin from {filepath}")
    else:
        print(f"Only 1 block found in {filepath}")

remove_old_dup(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
remove_old_dup(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
