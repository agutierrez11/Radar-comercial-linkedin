import re

def fix_dup(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find second occurrence of "async function enrichSingleContactLive("
    first_idx = content.find("async function enrichSingleContactLive(")
    if first_idx != -1:
        second_idx = content.find("async function enrichSingleContactLive(", first_idx + 30)
        if second_idx != -1:
            # Find the end of the second function block (ending before the next function definition)
            next_func = content.find("async function", second_idx + 30)
            if next_func == -1:
                next_func = content.find("function", second_idx + 30)
            if next_func != -1:
                content = content[:second_idx] + content[next_func:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_dup(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_dup(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
