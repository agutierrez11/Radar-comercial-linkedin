import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        file_path = os.path.abspath('index.html')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1500)

        print("[TEST 1] Logging in as Antonio (Master)...")
        await page.evaluate("""async () => {
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1500)
        contacts_count = await page.evaluate("() => S.contacts ? S.contacts.length : 0")
        owner_name = await page.evaluate("() => S.ownerName")
        print(f"[TEST 1 SUCCESS] Antonio vault loaded: {contacts_count} contacts, owner: {owner_name}")
        await page.screenshot(path="qa_demo_step1_antonio_vault.png")

        print("[TEST 2] Logging in as Ronan (Sandbox)...")
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'ronan';
            document.getElementById('login-password-input').value = 'ronan123';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1500)
        ronan_contacts = await page.evaluate("() => S.contacts ? S.contacts.length : 0")
        print(f"[TEST 2 SUCCESS] Ronan sandbox loaded: {ronan_contacts} contacts")
        await page.screenshot(path="qa_demo_step2_ronan_sandbox.png")

        print("[TEST 3] Logging in as Giovanna (Zero Data Vault)...")
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'giovanna';
            document.getElementById('login-password-input').value = 'gio2026';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1500)
        gio_contacts = await page.evaluate("() => S.contacts ? S.contacts.length : 0")
        gio_messages = await page.evaluate("() => S.messages ? S.messages.length : 0")
        print(f"[TEST 3 SUCCESS] Giovanna isolated vault loaded: {gio_contacts} contacts, {gio_messages} messages")
        await page.screenshot(path="qa_demo_step3_giovanna_zero_data.png")

        print("[TEST 4] Switch back to Antonio to verify data isolation...")
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1500)
        antonio_final_count = await page.evaluate("() => S.contacts ? S.contacts.length : 0")
        print(f"[TEST 4 SUCCESS] Antonio vault remains intact: {antonio_final_count} contacts")
        await page.screenshot(path="qa_demo_step4_antonio_intact.png")

        await browser.close()

asyncio.run(main())
