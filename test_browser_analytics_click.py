from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    # Auto authenticate as Master
    page.evaluate("if (typeof loadDemoData === 'function') loadDemoData();")
    page.evaluate("if (typeof unlockAnalyticsUI === 'function') unlockAnalyticsUI();")
    
    page.wait_for_timeout(500)
    
    # Click Analítica RevOps
    page.click('[data-section="analytics"]')
    page.wait_for_timeout(500)
    
    # Take screenshot of analytics section
    page.screenshot(path="analytics_qa_screenshot.png")
    
    # Check visibility of analytics-locked and analytics-dashboard and containers
    vis_a = page.evaluate("document.getElementById('analytics-view-container-a') ? document.getElementById('analytics-view-container-a').style.display : 'N/A'")
    vis_b = page.evaluate("document.getElementById('analytics-view-container-b') ? document.getElementById('analytics-view-container-b').style.display : 'N/A'")
    vis_locked = page.evaluate("document.getElementById('analytics-locked') ? document.getElementById('analytics-locked').style.display : 'N/A'")
    vis_dash = page.evaluate("document.getElementById('analytics-dashboard') ? document.getElementById('analytics-dashboard').style.display : 'N/A'")
    
    print(f"vis_a: '{vis_a}', vis_b: '{vis_b}', vis_locked: '{vis_locked}', vis_dash: '{vis_dash}'")
    
    browser.close()
