import re
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
        
        // Let's test different criteria combinations
        const contacts = S.contacts;
        
        // Count per individual criterion
        const counts = {};
        S.criteria.forEach(cr => {
            counts[cr.id] = contacts.filter(c => cr.fn(c)).length;
        });
        
        return { total: contacts.length, counts: counts };
    }""")
    print("Individual criteria counts:", res)
    browser.close()
