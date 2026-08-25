import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(500)
    
    res = page.evaluate("""() => {
      const pillBefore = document.getElementById('active-user-name').textContent;
      if (typeof window.submitCustomLogin === 'function') {
        window.submitCustomLogin('giovanna');
      } else if (typeof submitCustomLogin === 'function') {
        submitCustomLogin('giovanna');
      }
      const pillAfter = document.getElementById('active-user-name').textContent;
      const userObj = window.currentAuthUser;
      return { pillBefore, pillAfter, userObj };
    }""")
    print("Submit login trace:", res)
    browser.close()
