import subprocess, re
from playwright.sync_api import sync_playwright

# Get all commit hashes from today and yesterday
commits_raw = subprocess.check_output(['git', 'log', '--oneline', '-n', '30'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
commits = [line.split()[0] for line in commits_raw.strip().split('\n')]

print(f"Checking {len(commits)} commits for Dunbar counts...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for c in commits:
        try:
            content = subprocess.check_output(['git', 'show', f'{c}:index.html'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
            with open('temp_commit.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            page = browser.new_page()
            page.goto("file:///c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial/temp_commit.html")
            page.wait_for_timeout(400)
            
            res = page.evaluate("""async () => {
                if (typeof submitCustomLogin === 'function') {
                    const u = document.getElementById('login-username-input');
                    if (u) u.value = 'antonio';
                    const p = document.getElementById('login-password-input');
                    if (p) p.value = '12345';
                    await submitCustomLogin();
                }
                
                if (typeof S === 'undefined' || !S.contacts || S.contacts.length === 0) return null;
                const contacts = S.contacts;
                
                const activePurgeCandidates = contacts.filter(c => {
                    if (c.whitelisted || c.discardedFromPurge || c.crmStatus === 'Descartado') return false;
                    return S.criteria.filter(cr => cr.on).some(cr => cr.fn(c));
                }).length;
                
                const activeOnCriteria = S.criteria.filter(cr => cr.on).map(cr => cr.id);
                
                return { total: contacts.length, activePurgeCandidates, activeOnCriteria };
            }""")
            page.close()
            print(f"Commit {c}: {res}")
        except Exception as err:
            print(f"Commit {c} failed: {err}")

    browser.close()
