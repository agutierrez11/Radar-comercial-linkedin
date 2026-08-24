from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    info = page.evaluate("""() => {
      if (typeof window.navigate === 'function') {
        window.navigate('analytics');
      }
      const el = document.getElementById('sec-analytics');
      if (!el) return 'sec-analytics NOT FOUND IN DOM';
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      return {
        id: el.id,
        className: el.className,
        display: style.display,
        visibility: style.visibility,
        rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        parentTag: el.parentElement.tagName,
        parentId: el.parentElement.id,
        parentDisplay: window.getComputedStyle(el.parentElement).display,
        childrenCount: el.children.length,
        lockedDisplay: document.getElementById('analytics-locked') ? document.getElementById('analytics-locked').style.display : 'NO LOCKED',
        dashboardDisplay: document.getElementById('analytics-dashboard') ? document.getElementById('analytics-dashboard').style.display : 'NO DASHBOARD'
      };
    }""")
    print("Sec Analytics Info:", info)
    
    page.screenshot(path="live_sec_analytics_debug.png")
    print("Saved live_sec_analytics_debug.png")
    
    browser.close()
