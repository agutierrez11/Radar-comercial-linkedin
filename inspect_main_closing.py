import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

main_end = content.find('</main>')
sec_analytics = content.find('id="sec-analytics"')

print(f"main_end index: {main_end}")
print(f"sec_analytics index: {sec_analytics}")

if sec_analytics > main_end:
    print("CRITICAL BUG CONFIRMED: sec-analytics IS LOCATED AFTER </main>!")
else:
    print("sec-analytics is before </main>.")
