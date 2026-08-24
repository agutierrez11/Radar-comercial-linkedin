import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("function renderAnalytics()")
if idx != -1:
    print(content[idx:idx+1500])
else:
    print("function renderAnalytics() NOT FOUND!")

idx2 = content.find("function unlockAnalyticsUI()")
if idx2 != -1:
    print("--- UNLOCK ANALYTICS ---")
    print(content[idx2:idx2+1000])
