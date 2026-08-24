from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal();")
    
    page.evaluate("navigate('analytics');")
    page.wait_for_timeout(500)
    
    sec_info = page.evaluate("""() => {
      const el = document.getElementById('sec-analytics');
      if (!el) return 'NOT FOUND';
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      return {
        className: el.className,
        display: style.display,
        visibility: style.visibility,
        rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        childrenCount: el.children.length,
        parent: el.parentElement.id || el.parentElement.tagName
      };
    }""")
    print("sec-analytics info:", sec_info)
    
    browser.close()
