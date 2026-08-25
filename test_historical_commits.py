import subprocess, re
from playwright.sync_api import sync_playwright

commits = ['952fed9', '0018d4d', '19c8326', 'eed7fec', '26f8973', '774b30e']

for c in commits:
    try:
        content = subprocess.check_output(['git', 'show', f'{c}:index.html'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
        with open('temp_commit.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("file:///c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial/temp_commit.html")
            page.wait_for_timeout(500)
            
            res = page.evaluate("""async () => {
                if (typeof submitCustomLogin === 'function') {
                    const u = document.getElementById('login-username-input');
                    if (u) u.value = 'antonio';
                    const p = document.getElementById('login-password-input');
                    if (p) p.value = '12345';
                    await submitCustomLogin();
                }
                
                if (typeof S === 'undefined' || !S.contacts) return null;
                const contacts = S.contacts;
                
                // Active purge criteria
                const activePurgeCandidates = contacts.filter(c => {
                    if (c.whitelisted || c.discardedFromPurge || c.crmStatus === 'Descartado') return false;
                    return S.criteria.filter(cr => cr.on).some(cr => cr.fn(c));
                }).length;
                
                const criteriaCounts = {};
                S.criteria.forEach(cr => {
                    criteriaCounts[cr.id] = { label: cr.label, on: cr.on, count: contacts.filter(c => cr.fn(c)).length };
                });
                
                return { total: contacts.length, activePurgeCandidates, criteriaCounts };
            }""")
            print(f"Commit {c}:", res)
            browser.close()
    except Exception as err:
        print(f"Commit {c} failed: {err}")
