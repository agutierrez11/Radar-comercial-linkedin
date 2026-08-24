import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal();")
    page.evaluate("if (typeof loadDemoData === 'function') loadDemoData();")
    page.click('[data-section="analytics"]')
    page.wait_for_timeout(1000)
    
    boxes = page.evaluate("""
        const getBox = id => {
            const el = document.getElementById(id);
            if (!el) return null;
            const rect = el.getBoundingClientRect();
            return {
                id,
                x: rect.x, y: rect.y,
                width: rect.width, height: rect.height,
                top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right
            };
        };
        [
            getBox('app-shell'),
            getBox('main-content'),
            getBox('sec-analytics'),
            getBox('analytics-view-container-a'),
            getBox('analytics-dashboard')
        ];
    """)
    
    for b in boxes:
        print(b)
        
    browser.close()
