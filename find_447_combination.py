from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{'c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial/index.html'}")
    page.wait_for_timeout(1000)
    
    res = page.evaluate("""async () => {
        document.getElementById('login-username-input').value = 'antonio';
        document.getElementById('login-password-input').value = '12345';
        await submitCustomLogin();
        
        const contacts = S.contacts;
        
        // Let's test combinations of criteria flags
        // For example, what if old_cold connects > 3 years, > 5 years, or what if crmStatus === 'Descartado' already reduced 2953?
        // Let's check how many total contacts are in S.contacts
        // Let's test if turning on old_cold with different years gives 447
        
        const results = [];
        for (let years of [1, 2, 3, 4, 5]) {
            const count = contacts.filter(c => {
                if (c.msg_count && c.msg_count > 0) return false;
                if (c.connectedYearsAgo <= years) return false;
                if (c.hierarchy === 'C-Level' || c.hierarchy === 'Director' || c.hierarchy === 'Gerente') return false;
                if (c.email) return false;
                if (['Fintech/Pagos', 'SaaS/Tech', 'Retail/eCommerce'].includes(c.sector)) return false;
                return true;
            }).length;
            results.push({ years, count });
        }
        
        // Also check if crmStatus !== 'Descartado' reduces total
        const discardedCount = contacts.filter(c => c.crmStatus === 'Descartado' || c.discardedFromPurge).length;
        
        return { total: contacts.length, discardedCount, oldColdYears: results };
    }""")
    print("Combinations analysis:", res)
    browser.close()
