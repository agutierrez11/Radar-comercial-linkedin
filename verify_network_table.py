import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1100})
        
        file_path = os.path.abspath('index.html')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1500)

        # Login and navigate explicitly to network
        await page.evaluate("""async () => {
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
            if (typeof navigate === 'function') navigate('network');
        }""")
        
        await page.wait_for_timeout(2000)

        # Scroll to network table
        table_el = page.locator('#net-table')
        if await table_el.count() > 0:
            await table_el.scroll_into_view_if_needed()

        await page.wait_for_timeout(1000)
        # Take screenshot of network table
        await page.screenshot(path="qa_network_table_populated.png")
        print("[SUCCESS] Table screenshot captured successfully: qa_network_table_populated.png")
        await browser.close()

asyncio.run(main())
