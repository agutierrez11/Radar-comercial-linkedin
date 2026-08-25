import re

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix toggleVerifiedFilter to handle un-enriched dataset gracefully
    old_toggle = """function toggleVerifiedFilter() {
  filterVerifiedOnly = !filterVerifiedOnly;
  const btn = document.getElementById('btn-filter-verified');
  if (btn) {
    if (filterVerifiedOnly) {
      btn.style.background = 'var(--green)';
      btn.style.color = '#fff';
    } else {
      btn.style.background = 'var(--surface)';
      btn.style.color = 'var(--green)';
    }
  }
  applyNetworkFilters();
}"""

    new_toggle = """function toggleVerifiedFilter() {
  const enrichedCount = (S.contacts || []).filter(c => c.harvest_enriched).length;
  if (!filterVerifiedOnly && enrichedCount === 0) {
    if (typeof showToast === 'function') {
      showToast('ℹ️ Aún no has ejecutado el enriquecimiento Live (HarvestAPI) para tus contactos. Mostrando todos los contactos de la Bóveda.', 'ℹ️');
    }
    filterVerifiedOnly = false;
    const btn = document.getElementById('btn-filter-verified');
    if (btn) {
      btn.style.background = 'var(--surface)';
      btn.style.color = 'var(--green)';
    }
    applyNetworkFilters();
    return;
  }
  
  filterVerifiedOnly = !filterVerifiedOnly;
  const btn = document.getElementById('btn-filter-verified');
  if (btn) {
    if (filterVerifiedOnly) {
      btn.style.background = 'var(--green)';
      btn.style.color = '#fff';
    } else {
      btn.style.background = 'var(--surface)';
      btn.style.color = 'var(--green)';
    }
  }
  applyNetworkFilters();
}"""

    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)
        print("Replaced toggleVerifiedFilter successfully.")

    # 2. Sanitize criteria loading in restoreLocalVault so old_cold is ALWAYS false by default on initial vault restore
    old_restore_check = "if (data.crmState) S.crmState = data.crmState;"
    new_restore_check = """if (data.crmState) S.crmState = data.crmState;
        // Ensure aggressive old_cold criterion is OFF by default on load unless explicitly turned on by user
        if (S.criteria) {
          S.criteria.forEach(cr => {
            if (cr.id === 'old_cold' || cr.id === 'no_country') cr.on = false;
          });
        }"""

    if old_restore_check in content:
        content = content.replace(old_restore_check, new_restore_check)
        print("Added criteria sanitization in restoreLocalVault.")

    # 3. Also ensure window.filterVerifiedOnly is always initialized to false
    content = content.replace("filterVerifiedOnly = true;", "filterVerifiedOnly = false;")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}")

patch_file('index.html')
patch_file('staging.html')
