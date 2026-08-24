import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for sec-analytics HTML structure
analytics_sec = re.findall(r'<section[^>]*id=["\']sec-analytics["\'][\s\S]*?</section>', content)
print(f"Found {len(analytics_sec)} sec-analytics blocks.")
if analytics_sec:
    print("--- SEC ANALYTICS FIRST 500 CHARS ---")
    print(analytics_sec[0][:500])

# Search for navigate function
nav_match = re.search(r'function navigate\(.*?\{[\s\S]*?\n\}', content)
if nav_match:
    print("--- NAVIGATE FUNCTION ---")
    print(nav_match.group(0)[:800])
