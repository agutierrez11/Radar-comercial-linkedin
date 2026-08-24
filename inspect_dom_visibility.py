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
    
    # Inspect all parent elements of sec-analytics up to body
    hierarchy_info = page.evaluate("""
        const el = document.getElementById('sec-analytics');
        const parents = [];
        let curr = el;
        while(curr) {
            const cs = window.getComputedStyle(curr);
            parents.push({
                tag: curr.tagName,
                id: curr.id,
                className: curr.className,
                display: cs.display,
                visibility: cs.visibility,
                opacity: cs.opacity,
                height: curr.offsetHeight,
                width: curr.offsetWidth
            });
            curr = curr.parentElement;
        }
        parents;
    """)
    
    for item in hierarchy_info:
        print(item)
        
    browser.close()
