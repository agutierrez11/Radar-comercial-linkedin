import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    res = page.evaluate("""() => {
      console.log('--- EXECUTING GIOVANNA LOGIN ---');
      window.submitCustomLogin('giovanna');
      const pill = document.getElementById('active-user-name');
      return {
        pillText: pill ? pill.textContent : 'NO PILL',
        userObj: window.currentAuthUser
      };
    }""")
    print("Execution result:", res)
    browser.close()
