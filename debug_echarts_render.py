from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal();")
    page.evaluate("if (typeof loadDemoData === 'function') loadDemoData();")
    page.evaluate("navigate('analytics');")
    page.evaluate("switchAnalyticsViewMode('B');")
    page.wait_for_timeout(1000)
    
    # Check if echarts object exists
    echarts_exists = page.evaluate("typeof echarts")
    print(f"typeof echarts: {echarts_exists}")
    
    # Force call renderPowerBiEcharts
    page.evaluate("renderPowerBiEcharts();")
    page.wait_for_timeout(500)
    
    # Check if canvas elements were inserted into echart-funnel
    canvas_count = page.evaluate("document.querySelectorAll('#echart-funnel canvas').length")
    print(f"Canvas count in echart-funnel: {canvas_count}")
    
    browser.close()
