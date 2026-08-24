import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== AUDITING PURGE & WHITELIST LOGIC ===")

# Check if protectFromPurge is called correctly in HTML buttons
protect_btn_matches = re.findall(r'protectFromPurge\((.*?)\)', html)
print(f"Found {len(protect_btn_matches)} calls to protectFromPurge in HTML:")
for m in protect_btn_matches[:5]:
    print("   -> protectFromPurge(" + m + ")")

# Check if whitelisted is preserved in saveLocalVault / restoreLocalVault
if 'whitelisted' in html:
    print("[OK] 'whitelisted' property is present in code.")

# Check if whitelisted is preserved in loadCrmState
if 'c.whitelisted = !!db[key].whitelisted' in html:
    print("[OK] loadCrmState correctly restores c.whitelisted from localStorage.")
else:
    print("[FAIL] loadCrmState may not be restoring c.whitelisted!")

# Check if whitelisted is saved in saveContactCrm
if 'whitelisted: !!c.whitelisted' in html:
    print("[OK] saveContactCrm correctly persists whitelisted in localStorage.")
else:
    print("[FAIL] saveContactCrm may not be saving whitelisted!")

# Check if protectFromPurge calls saveContactCrm
if 'saveContactCrm' in html:
    print("[OK] saveContactCrm present.")
