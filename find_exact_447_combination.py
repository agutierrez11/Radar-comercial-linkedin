from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial/index.html")
    page.wait_for_timeout(1000)
    
    res = page.evaluate("""async () => {
        document.getElementById('login-username-input').value = 'antonio';
        document.getElementById('login-password-input').value = '12345';
        await submitCustomLogin();
        
        const contacts = S.contacts;
        const criteria = S.criteria;
        
        // Try all 2^7 combinations of criteria.on
        const matches = [];
        const n = criteria.length;
        for (let i = 0; i < (1 << n); i++) {
            const activeFlags = [];
            for (let j = 0; j < n; j++) {
                if ((i & (1 << j)) !== 0) activeFlags.push(criteria[j]);
            }
            
            const candidateCount = contacts.filter(c => {
                if (c.whitelisted || c.discardedFromPurge || c.crmStatus === 'Descartado') return false;
                return activeFlags.some(cr => cr.fn(c));
            }).length;
            
            if (candidateCount >= 400 && candidateCount <= 500) {
                matches.push({
                    count: candidateCount,
                    active: activeFlags.map(x => x.label)
                });
            }
        }
        return matches;
    }""")
    print("Combinations matching ~447 candidates:")
    for m in res:
        print(f"Count: {m['count']} | Active criteria: {m['active']}")
    browser.close()
