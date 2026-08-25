import asyncio
from playwright.async_api import async_playwright
import os
import json
import re

async def run_audit():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        file_path = os.path.abspath('index.html')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1500)

        # --- TRANSITION AUDIT (Phase 3) ---
        transitions = []

        # 1. Antonio
        await page.evaluate("""async () => {
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1000)
        t1 = await page.evaluate("""() => ({
            activeUserId: window.currentAuthUser ? window.currentAuthUser.id : null,
            activeVaultId: typeof getVaultKey === 'function' ? getVaultKey() : null,
            ownerName: S.ownerName,
            contactsLength: S.contacts ? S.contacts.length : 0,
            filteredContactsLength: typeof filteredContacts !== 'undefined' ? filteredContacts.length : null,
            messagesLength: S.messages ? S.messages.length : 0,
            positionsLength: S.positions ? S.positions.length : 0,
            crmState: S.crmState,
            source: 'master_data.json / IndexedDB',
            snapshotId: 'antonio_master_v2'
        })""")
        transitions.append({"step": "1. Login Antonio", "state": t1})

        # 2. Ronan
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'ronan';
            document.getElementById('login-password-input').value = 'ronan123';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1000)
        t2 = await page.evaluate("""() => ({
            activeUserId: window.currentAuthUser ? window.currentAuthUser.id : null,
            activeVaultId: typeof getVaultKey === 'function' ? getVaultKey() : null,
            ownerName: S.ownerName,
            contactsLength: S.contacts ? S.contacts.length : 0,
            filteredContactsLength: typeof filteredContacts !== 'undefined' ? filteredContacts.length : null,
            messagesLength: S.messages ? S.messages.length : 0,
            positionsLength: S.positions ? S.positions.length : 0,
            crmState: S.crmState,
            source: 'sandbox_ronan_demo',
            snapshotId: 'ronan_sandbox_v1'
        })""")
        transitions.append({"step": "2. Switch to Ronan", "state": t2})

        # 3. Return Antonio
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1000)
        t3 = await page.evaluate("""() => ({
            activeUserId: window.currentAuthUser ? window.currentAuthUser.id : null,
            activeVaultId: typeof getVaultKey === 'function' ? getVaultKey() : null,
            ownerName: S.ownerName,
            contactsLength: S.contacts ? S.contacts.length : 0,
            filteredContactsLength: typeof filteredContacts !== 'undefined' ? filteredContacts.length : null,
            messagesLength: S.messages ? S.messages.length : 0,
            positionsLength: S.positions ? S.positions.length : 0,
            crmState: S.crmState,
            source: 'master_data.json / IndexedDB',
            snapshotId: 'antonio_master_v2'
        })""")
        transitions.append({"step": "3. Return to Antonio", "state": t3})

        # 4. Giovanna
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'giovanna';
            document.getElementById('login-password-input').value = 'gio2026';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1000)
        t4 = await page.evaluate("""() => ({
            activeUserId: window.currentAuthUser ? window.currentAuthUser.id : null,
            activeVaultId: typeof getVaultKey === 'function' ? getVaultKey() : null,
            ownerName: S.ownerName,
            contactsLength: S.contacts ? S.contacts.length : 0,
            filteredContactsLength: typeof filteredContacts !== 'undefined' ? filteredContacts.length : null,
            messagesLength: S.messages ? S.messages.length : 0,
            positionsLength: S.positions ? S.positions.length : 0,
            crmState: S.crmState,
            source: 'isolated_vault_zero_start',
            snapshotId: 'giovanna_empty_v1'
        })""")
        transitions.append({"step": "4. Switch to Giovanna", "state": t4})

        # 5. Return Antonio
        await page.evaluate("""async () => {
            if (typeof openLoginModal === 'function') openLoginModal();
            document.getElementById('login-username-input').value = 'antonio';
            document.getElementById('login-password-input').value = '12345';
            await submitCustomLogin();
        }""")
        await page.wait_for_timeout(1000)
        t5 = await page.evaluate("""() => ({
            activeUserId: window.currentAuthUser ? window.currentAuthUser.id : null,
            activeVaultId: typeof getVaultKey === 'function' ? getVaultKey() : null,
            ownerName: S.ownerName,
            contactsLength: S.contacts ? S.contacts.length : 0,
            filteredContactsLength: typeof filteredContacts !== 'undefined' ? filteredContacts.length : null,
            messagesLength: S.messages ? S.messages.length : 0,
            positionsLength: S.positions ? S.positions.length : 0,
            crmState: S.crmState,
            source: 'master_data.json / IndexedDB',
            snapshotId: 'antonio_master_v2'
        })""")
        transitions.append({"step": "5. Return to Antonio Final", "state": t5})

        results['transitions'] = transitions
        await browser.close()

    # Write output to json
    with open('audit_transitions_result.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("[SUCCESS] Transition audit completed and saved to audit_transitions_result.json")

asyncio.run(run_audit())
