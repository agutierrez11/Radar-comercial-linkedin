import json

with open('enriched_connections.json', 'r', encoding='utf-8') as f:
    contacts = json.load(f)

# Assign IDs like buildContacts does:
for i, c in enumerate(contacts):
    c['id'] = i

def norm(text):
    if not text: return ""
    return str(text).lower().strip()

def get_contact_crm_key(c):
    url = c.get('url') or ''
    if url and len(url.strip()) > 0:
        return url.strip()
    name = c.get('originalName') or c.get('name') or c.get('full_name') or ''
    company = c.get('originalCompany') or c.get('company') or ''
    return f"{norm(name)}|{norm(company)}"

# Criteria for 'Sin empresa registrada'
def cr_sin_empresa(c):
    comp = c.get('company') or ''
    return not comp or comp.strip() == '' or norm(comp) == 'sin empresa' or 'sin empresa' in norm(comp)

def is_purge_candidate(c):
    if c.get('whitelisted') or c.get('discardedFromPurge') or c.get('crmStatus') == 'Descartado':
        return False
    return cr_sin_empresa(c)

print("--- INITIAL CANDIDATES FOR 'SIN EMPRESA' ---")
candidates = [c for c in contacts if is_purge_candidate(c)]
print(f"Total candidates: {len(candidates)}")

targets = [c for c in candidates if any(k in norm(c.get('name') or c.get('full_name')) for k in ['estefany', 'nicolau', 'anurag'])]
print(f"Targets found in candidates: {[c.get('name') or c.get('full_name') for c in targets]}")

# SIMULATE CLICKING MANTENER ON TARGET 0
t0 = targets[0]
target_id = t0['id']
print(f"\nClicking 'Mantener' on target: {t0.get('name') or t0.get('full_name')} (ID: {target_id})...")

# protectFromPurge logic
c_found = next((x for x in contacts if str(x['id']) == str(target_id)), None)
if c_found:
    c_found['whitelisted'] = True
    c_found['discardedFromPurge'] = False
    print("Set c_found['whitelisted'] = True")

print(f"After protectFromPurge, is_purge_candidate({c_found.get('name') or c_found.get('full_name')}) = {is_purge_candidate(c_found)}")

candidates_after = [c for c in contacts if is_purge_candidate(c)]
print(f"Total candidates after click: {len(candidates_after)}")
print(f"Is target still in candidates? {any(c['id'] == target_id for c in candidates_after)}")
