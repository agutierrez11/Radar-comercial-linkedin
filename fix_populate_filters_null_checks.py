import re

def fix_populate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_populate = """function populateFilters() {
  const countries = [...new Set(S.contacts.map(c => getCanonicalCountry(c.country)))].sort();
  const sel = document.getElementById('net-country');
  sel.innerHTML = '<option value="">🌎 Todos los países</option>';
  countries.forEach(c => {
    const o = document.createElement('option'); o.value = c;
    o.textContent = countryFlag(c); sel.appendChild(o);
  });
  const sectors = [...new Set(S.contacts.map(c => c.sector)))].sort();
  const sels = document.getElementById('net-sector');
  sels.innerHTML = '<option value="">🏭 Todos los sectores</option>';"""

    # Replace with safe null checks
    old_block = """function populateFilters() {"""
    new_block = """function populateFilters() {
  const countries = [...new Set((S.contacts||[]).map(c => getCanonicalCountry(c ? c.country : '')))].filter(Boolean).sort();
  const sel = document.getElementById('net-country');
  if (sel) {
    sel.innerHTML = '<option value="">🌎 Todos los países</option>';
    countries.forEach(c => {
      const o = document.createElement('option'); o.value = c;
      o.textContent = countryFlag(c); sel.appendChild(o);
    });
  }
  const sectors = [...new Set((S.contacts||[]).map(c => c ? c.sector : ''))].filter(Boolean).sort();
  const sels = document.getElementById('net-sector');
  if (sels) {
    sels.innerHTML = '<option value="">🏭 Todos los sectores</option>';
    sectors.forEach(s => {
      const o = document.createElement('option'); o.value = s; o.textContent = s; sels.appendChild(o);
    });
  }"""

    # Clean lines 3745-3758
    content = re.sub(
        r'function populateFilters\(\)\s*\{[\s\S]*?// Populate ICP Role Selector',
        new_block + "\n\n  // Populate ICP Role Selector",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_populate(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
fix_populate(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("OK")
