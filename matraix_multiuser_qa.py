import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    print("\n--- TEST 1: FRESH PAGE LOAD AUTH GATING ---")
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    modal_info = page.evaluate("""() => {
      const modal = document.getElementById('login-modal');
      const main = document.getElementById('main-content');
      return {
        modalDisplay: window.getComputedStyle(modal).display,
        modalZIndex: window.getComputedStyle(modal).zIndex,
        mainVisibility: window.getComputedStyle(main).visibility,
        mainOpacity: window.getComputedStyle(main).opacity
      };
    }""")
    print("Modal gating state:", modal_info)
    assert modal_info['modalDisplay'] == 'flex', "Modal must be display: flex on load"
    assert modal_info['mainOpacity'] == '0', "Main content must be opacity: 0 before login"
    page.screenshot(path="qa_test1_fresh_login_gating.png")
    print("PASSED TEST 1: Zero-flash login gating verified!")

    print("\n--- TEST 2: GIOVANNA ISOLATED LOGIN ---")
    page.evaluate("submitCustomLogin('giovanna');")
    page.wait_for_timeout(1000)
    
    gio_info = page.evaluate("""() => {
      const activeUser = document.getElementById('active-user-name').textContent;
      const stateObj = window.S || (typeof S !== 'undefined' ? S : {});
      const contactsCount = stateObj.contacts ? stateObj.contacts.length : 0;
      const adminDropdown = document.getElementById('admin-vault-dropdown');
      const pillContainer = document.getElementById('active-user-pill');
      return {
        activeUser,
        contactsCount,
        dropdownDisplay: adminDropdown ? adminDropdown.style.display : 'NONE',
        pillCursor: pillContainer ? pillContainer.style.cursor : 'default'
      };
    }""")
    print("Giovanna vault state:", gio_info)
    assert gio_info['contactsCount'] == 0, "Giovanna vault must have 0 contacts"
    assert "Giovanna" in gio_info['activeUser'], f"Active user must be Giovanna, got {gio_info['activeUser']}"
    page.screenshot(path="qa_test2_giovanna_isolated_vault.png")
    print("PASSED TEST 2: Giovanna isolated vault verified!")

    print("\n--- TEST 3: ANTONIO MASTER ADMIN LOGIN ---")
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    page.evaluate("submitCustomLogin('antonio');")
    page.wait_for_timeout(1500)
    
    antonio_info = page.evaluate("""() => {
      const activeUser = document.getElementById('active-user-name').textContent;
      const stateObj = window.S || (typeof S !== 'undefined' ? S : {});
      const contactsCount = stateObj.contacts ? stateObj.contacts.length : 0;
      const isMaster = window.currentAuthUser ? window.currentAuthUser.isMaster : false;
      return {
        activeUser,
        contactsCount,
        isMaster
      };
    }""")
    print("Antonio master state:", antonio_info)
    assert antonio_info['contactsCount'] >= 2900, "Antonio master must have ~2,953 contacts"
    assert antonio_info['isMaster'] == True, "Antonio must be Master Admin"
    page.screenshot(path="qa_test3_antonio_master_admin.png")
    print("PASSED TEST 3: Antonio Master Admin verified!")
    
    browser.close()
    print("\n✅ ALL 3 MULTI-USER AUTHENTICATION QA TESTS PASSED PERFECTLY!")
