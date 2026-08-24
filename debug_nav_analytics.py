from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal();")
    
    res = page.evaluate("""() => {
      console.log('BEFORE NAV:', window.currentActiveSection, S.activeSection);
      if (typeof window.navigate === 'function') {
        window.navigate('analytics');
      } else if (typeof navigate === 'function') {
        navigate('analytics');
      }
      const secAna = document.getElementById('sec-analytics');
      return {
        activeSection: S.activeSection,
        secAnaClass: secAna ? secAna.className : 'NOT FOUND'
      };
    }""")
    print("Nav result:", res)
    
    page.wait_for_timeout(500)
    page.screenshot(path="debug_nav_analytics.png")
    
    browser.close()
