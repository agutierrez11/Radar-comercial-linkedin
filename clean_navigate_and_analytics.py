import re

def clean_navigate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean top function navigate duplicate if any
    content = re.sub(r'function navigate\(secId\)\s*\{[\s\S]*?\}\n', '', content)

    # 2. Update navigate(sec) at line 3668
    old_nav_block = """function navigate(sec) {
  if (REQUIRES_ZIP.includes(sec) && !S.loadedParts.connections) {
    alert("⚠️ Carga primero tu archivo de contactos (Connections.csv) para habilitar esta sección.");
    return;
  }
  S.activeSection = sec;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('sec-' + sec).classList.add('active');
  document.querySelector(`[data-section="${sec}"]`).classList.add('active');"""

    new_nav_block = """function navigate(sec) {
  if (typeof REQUIRES_ZIP !== 'undefined' && REQUIRES_ZIP.includes(sec) && !S.loadedParts.connections) {
    alert("⚠️ Carga primero tu archivo de contactos (Connections.csv) para habilitar esta sección.");
    return;
  }
  S.activeSection = sec;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const targetSec = document.getElementById('sec-' + sec);
  if (targetSec) targetSec.classList.add('active');
  const navItem = document.querySelector(`[data-section="${sec}"]`);
  if (navItem) navItem.classList.add('active');"""

    content = content.replace(old_nav_block, new_nav_block)

    # 3. Add analytics unlock inside navigate(sec)
    old_ana_check = """  if (sec === 'analytics') {
    requestAnimationFrame(() => { renderAnalytics(); });
  }"""

    new_ana_check = """  if (sec === 'analytics') {
    const locked = document.getElementById('analytics-locked');
    const dashboard = document.getElementById('analytics-dashboard');
    if (locked) locked.style.display = 'none';
    if (dashboard) dashboard.style.display = 'block';
    requestAnimationFrame(() => {
      if (typeof renderAnalytics === 'function') renderAnalytics();
    });
  }"""

    content = content.replace(old_ana_check, new_ana_check)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clean_navigate(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\index.html")
clean_navigate(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial\staging.html")
print("Clean navigate patch applied!")
