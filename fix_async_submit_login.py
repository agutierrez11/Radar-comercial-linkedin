import re

def patch_submit_login(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Change function submitCustomLogin() to async function submitCustomLogin()
    content = content.replace("function submitCustomLogin() {", "async function submitCustomLogin() {")

    # 2. Change restoreLocalVault().then(...) to await restoreLocalVault()
    old_block = """    restoreLocalVault().then(async restored => {
      if (!restored) {"""

    new_block = """    const restored = await restoreLocalVault();
    if (!restored) {"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        # also remove the closing }); of the then block
        content = content.replace("""      if (typeof showToast === 'function') showToast(`👤 Bóveda Master Antonio cargada (${(S.contacts||[]).length.toLocaleString()} contactos).`, '🔑');
    });""", """      if (typeof showToast === 'function') showToast(`👤 Bóveda Master Antonio cargada (${(S.contacts||[]).length.toLocaleString()} contactos).`, '🔑');""")
        print(f"Patched submitCustomLogin to async/await in {filepath}")
    else:
        print(f"Old block not found in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_submit_login('index.html')
patch_submit_login('staging.html')
