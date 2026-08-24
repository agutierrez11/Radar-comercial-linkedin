import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("--- AUDITING ALL SIDEBAR BADGES & KPI COUNTERS ---")

badges = ['nb-network', 'nb-icp', 'nb-crm', 'nb-purge', 'nb-msgs']
for b in badges:
    matches = re.findall(rf"document\.getElementById\('{b}'\)\.textContent\s*=\s*(.+?);", html)
    print(f"Badge #{b}: {len(matches)} assignments found -> {matches}")

print("\n--- CHECKING CRM PIPELINE COUNTS ---")
crm_matches = re.findall(r"filter\([^\)]*crmStatus[^\)]*\)", html)
for m in crm_matches:
    print("CRM Filter:", m)
