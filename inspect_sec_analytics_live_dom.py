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
    
    html = page.evaluate("document.getElementById('sec-analytics') ? document.getElementById('sec-analytics').outerHTML : 'NULL'")
    print("--- SEC ANALYTICS OUTER HTML (FIRST 1000 CHARS) ---")
    print(html[:1000])
    
    browser.close()
