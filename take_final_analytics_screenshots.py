from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1500)
    
    # Click demo button in login modal if visible
    page.evaluate("""() => {
      const modal = document.getElementById('login-modal');
      if (modal) modal.style.display = 'none';
      if (typeof window.loadDemoData === 'function') window.loadDemoData(false);
    }""")
    page.wait_for_timeout(2500)
    
    # Click Analítica RevOps in sidebar
    page.evaluate("""() => {
      const item = document.querySelector('[data-section="analytics"]');
      if (item) item.click();
    }""")
    page.wait_for_timeout(1000)
    
    page.screenshot(path="final_analytics_vista_a.png")
    print("Vista A screenshot saved as final_analytics_vista_a.png!")
    
    # Switch to Vista B
    page.evaluate("""() => {
      if (typeof window.switchAnalyticsViewMode === 'function') window.switchAnalyticsViewMode('B');
    }""")
    page.wait_for_timeout(1500)
    
    page.screenshot(path="final_analytics_vista_b.png")
    print("Vista B screenshot saved as final_analytics_vista_b.png!")
    
    browser.close()
