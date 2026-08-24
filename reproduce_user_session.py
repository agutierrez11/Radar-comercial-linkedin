from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal();")
    page.evaluate("if (typeof loadDemoData === 'function') loadDemoData();")
    page.wait_for_timeout(500)
    
    # Click sidebar nav item to navigate to analytics
    page.evaluate("document.querySelector('[data-section=\"analytics\"]').click();")
    page.wait_for_timeout(500)
    
    # Click Vista B button via dispatch_event
    page.evaluate("document.getElementById('ana-mode-btn-b').click();")
    page.wait_for_timeout(1200)
    
    page.screenshot(path="user_session_analytics_vista_b_qa.png")
    print("Vista B screenshot taken successfully!")
    
    browser.close()
