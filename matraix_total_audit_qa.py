import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    print("\n=======================================================")
    print("      TOTAL TENANT ISOLATION & DATA LEAK AUDIT        ")
    print("=======================================================")

    print("\n--- AUDIT 1: FRESH PAGE LOAD ZERO-DATA LOCKOUT ---")
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    audit1 = page.evaluate("""() => {
      const modal = document.getElementById('login-modal');
      const main = document.getElementById('main-content');
      const contacts = window.S ? window.S.contacts.length : -1;
      const messages = window.S ? window.S.messages.length : -1;
      const positions = window.S ? window.S.positions.length : -1;
      return {
        modalDisplay: window.getComputedStyle(modal).display,
        mainOpacity: window.getComputedStyle(main).opacity,
        contacts,
        messages,
        positions
      };
    }""")
    print("Fresh load audit:", audit1)
    assert audit1['modalDisplay'] == 'flex', "Modal must be flex on load"
    assert audit1['mainOpacity'] == '0', "Main content must be hidden on load"
    assert audit1['contacts'] == 0, "Contacts must be 0 on fresh load"
    assert audit1['messages'] == 0, "Messages must be 0 on fresh load"
    assert audit1['positions'] == 0, "Positions must be 0 on fresh load"
    print("PASSED AUDIT 1: Zero-data startup lockout verified!")

    print("\n--- AUDIT 2: QUICK LOGIN BUTTONS ONLY POPULATE FIELDS (NO AUTO-SUBMIT) ---")
    page.evaluate("fillQuickLogin('antonio', '12345')")
    page.wait_for_timeout(500)
    audit2_quick = page.evaluate("""() => {
      const modal = document.getElementById('login-modal');
      const uVal = document.getElementById('login-username-input').value;
      const pVal = document.getElementById('login-password-input').value;
      return {
        modalDisplay: window.getComputedStyle(modal).display,
        uVal,
        pVal
      };
    }""")
    print("Quick login audit:", audit2_quick)
    assert audit2_quick['modalDisplay'] == 'flex', "Modal MUST remain visible (no auto-submit)"
    assert audit2_quick['uVal'] == 'antonio', "Username field must be populated"
    assert audit2_quick['pVal'] == '12345', "Password field must be populated"
    print("PASSED AUDIT 2: Quick buttons only populate fields without auto-submitting!")

    print("\n--- AUDIT 3: RONAN SANDBOX TENANT ISOLATION ---")
    page.fill("#login-username-input", "ronan")
    page.fill("#login-password-input", "ronan123")
    page.click("#login-submit-btn")
    page.wait_for_timeout(1000)
    
    audit3 = page.evaluate("""() => {
      const activeUser = document.getElementById('active-user-name').textContent;
      const ownerName = window.S ? window.S.ownerName : '';
      const contacts = window.S ? window.S.contacts.length : 0;
      const positions = window.S ? window.S.positions.length : 0;
      const messages = window.S ? window.S.messages || [] : [];
      const hasAntonioMsg = messages.some(m => {
        const txt = (m.CONTENT || m.content || '').toLowerCase();
        return txt.includes('clip') || txt.includes('fiserv') || txt.includes('attainment');
      });
      return {
        activeUser,
        ownerName,
        contacts,
        positions,
        messagesCount: messages.length,
        hasAntonioMsg
      };
    }""")
    print("Ronan audit state:", audit3)
    assert audit3['ownerName'] == 'Ronan', "Owner name must be Ronan"
    assert audit3['contacts'] == 500, "Ronan must have exactly 500 demo contacts"
    assert audit3['positions'] == 0, "Ronan must NOT have Antonio's career positions"
    assert audit3['hasAntonioMsg'] == False, "Ronan must NOT have Antonio's private messages"
    print("PASSED AUDIT 3: Ronan tenant isolation verified zero data leaks!")

    print("\n--- AUDIT 4: SWITCH FROM RONAN TO ANTONIO MASTER (ZERO LEAK VERIFICATION) ---")
    page.evaluate("openLoginModal()")
    page.wait_for_timeout(500)
    page.fill("#login-username-input", "antonio")
    page.fill("#login-password-input", "12345")
    page.click("#login-submit-btn")
    page.wait_for_timeout(1500)
    
    audit4 = page.evaluate("""() => {
      const activeUser = document.getElementById('active-user-name').textContent;
      const ownerName = window.S ? window.S.ownerName : '';
      const contacts = window.S ? window.S.contacts.length : 0;
      const positions = window.S ? window.S.positions.length : 0;
      const isMaster = window.currentAuthUser ? window.currentAuthUser.isMaster : false;
      const isRonanMode = window.isRonanAbMode || false;
      return {
        activeUser,
        ownerName,
        contacts,
        positions,
        isMaster,
        isRonanMode
      };
    }""")
    print("Antonio master after Ronan audit state:", audit4)
    assert audit4['isMaster'] == True, "Antonio must be Master Admin"
    assert audit4['isRonanMode'] == False, "Ronan AB mode must be FALSE when Antonio logs in"
    assert audit4['contacts'] >= 2900, "Antonio master must have ~2,953 contacts (NOT Ronan's 500 contacts)"
    assert audit4['positions'] == 6, "Antonio master must have 6 positions"
    print("PASSED AUDIT 4: Switching from Ronan to Antonio Master wipes Ronan state completely!")

    browser.close()
    print("\n=======================================================")
    print(" ✅ TOTAL AUDIT COMPLETE: ZERO DATA LEAKS VERIFIED!    ")
    print("=======================================================")
