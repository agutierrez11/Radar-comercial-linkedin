import re

def clean_duplicates(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all occurrences of function submitCustomLogin
    pattern = r'function submitCustomLogin\(targetUser\)\s*\{[\s\S]*?\n\}'
    matches = list(re.finditer(pattern, content))
    print(f"Found {len(matches)} matches in {filepath}")

    if len(matches) > 1:
        # Keep only the last complete definition and replace earlier ones
        last_match = matches[-1]
        content_before = content[:matches[0].start()]
        content_after = content[last_match.start():]
        content = content_before + content_after

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_duplicates(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
clean_duplicates(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Duplicate submitCustomLogin cleaned!")
