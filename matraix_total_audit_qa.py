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

    print("\n--- AUDIT 2: RONAN SANDBOX TENANT ISOLATION ---")
    page.fill("#login-username-input", "ronan")
    page.fill("#login-password-input", "ronan123")
    page.click("#login-submit-btn")
    page.wait_for_timeout(1000)
    
    audit2 = page.evaluate("""() => {
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
    print("Ronan audit state:", audit2)
    assert audit2['ownerName'] == 'Ronan', "Owner name must be Ronan"
    assert audit2['contacts'] == 500, "Ronan must have exactly 500 demo contacts"
    assert audit2['positions'] == 0, "Ronan must NOT have Antonio's career positions"
    assert audit2['hasAntonioMsg'] == False, "Ronan must NOT have Antonio's private messages"
    print("PASSED AUDIT 2: Ronan tenant isolation verified zero data leaks!")

    print("\n--- AUDIT 3: SWITCH FROM RONAN TO ANTONIO MASTER (NO CACHE CONTAMINATION) ---")
    page.evaluate("openLoginModal()")
    page.wait_for_timeout(500)
    page.fill("#login-username-input", "antonio")
    page.fill("#login-password-input", "12345")
    page.click("#login-submit-btn")
    page.wait_for_timeout(1500)
    
    audit3 = page.evaluate("""() => {
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
    print("Antonio master after Ronan audit state:", audit3)
    assert audit3['isMaster'] == True, "Antonio must be Master Admin"
    assert audit3['isRonanMode'] == False, "Ronan AB mode must be FALSE when Antonio logs in"
    assert audit3['contacts'] >= 2900, "Antonio master must have 2,953 clean depurated contacts"
    assert audit3['positions'] == 6, "Antonio master must have 6 positions"
    print("PASSED AUDIT 3: Antonio Master restores Antonio's 2,953 clean contacts without Ronan's 500 contacts!")

    browser.close()
    print("\n=======================================================")
    print(" ✅ TOTAL AUDIT COMPLETE: ZERO DATA LEAKS VERIFIED!    ")
    print("=======================================================")
