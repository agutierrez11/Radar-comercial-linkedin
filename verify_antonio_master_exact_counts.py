import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    page.fill("#login-username-input", "antonio")
    page.fill("#login-password-input", "12345")
    page.click("#login-submit-btn")
    page.wait_for_timeout(2000)
    
    res = page.evaluate("""() => {
      const activeContacts = (window.S.contacts || []).filter(c => c.crmStatus !== 'Descartado' && !c.discardedFromPurge);
      const totalRawContacts = window.S.contacts ? window.S.contacts.length : 0;
      const totalActiveContacts = activeContacts.length;
      
      const classAContacts = activeContacts.filter(c => c.score >= 60).length;
      
      const convSet = new Set();
      if (window.S.messages && window.S.messages.length > 0) {
        window.S.messages.forEach(m => {
          const cid = m.conv_id || m['CONVERSATION ID'] || m.CONVERSATION_ID || m.FROM || m.SENDER_NAME;
          if (cid) convSet.add(cid);
        });
      }
      const totalConversations = convSet.size;
      const totalRawMessages = window.S.messages ? window.S.messages.length : 0;
      
      const nbNetwork = document.getElementById('nb-network') ? document.getElementById('nb-network').textContent : '';
      const nbICP = document.getElementById('nb-icp') ? document.getElementById('nb-icp').textContent : '';
      const nbMsgs = document.getElementById('nb-msgs') ? document.getElementById('nb-msgs').textContent : '';
      const dunbarLabel = document.getElementById('dunbar-label') ? document.getElementById('dunbar-label').textContent : '';
      const hkpiTotal = document.getElementById('hkpi-total') ? document.getElementById('hkpi-total').textContent : '';
      
      return {
        totalRawContacts,
        totalActiveContacts,
        classAContacts,
        totalConversations,
        totalRawMessages,
        ui: {
          nbNetwork,
          nbICP,
          nbMsgs,
          dunbarLabel,
          hkpiTotal
        }
      };
    }""")
    
    print("\n=======================================================")
    print("      EXACT CONTEXT COUNTS FOR ANTONIO MASTER VAULT     ")
    print("=======================================================")
    print(f"Total Contactos (Raw): {res['totalRawContacts']}")
    print(f"Total Contactos (Activos desc. descartados): {res['totalActiveContacts']}")
    print(f"Total Mensajes Reales (Raw): {res['totalRawMessages']:,}")
    print(f"Total Conversaciones Identificadas: {res['totalConversations']:,}")
    print(f"Contactos Clase A / Dunbar (Score ≥ 60): {res['classAContacts']}")
    print("\n--- VALORES RENDERIZADOS EN LA INTERFAZ (DOM) ---")
    print(f"Header Total Pill (hkpi-total): {res['ui']['hkpiTotal']}")
    print(f"Sidebar Mi Red (nb-network): {res['ui']['nbNetwork']}")
    print(f"Sidebar ICP / Leads (nb-icp): {res['ui']['nbICP']}")
    print(f"Sidebar Mensajes (nb-msgs): {res['ui']['nbMsgs']}")
    print(f"Dunbar Progress Label: {res['ui']['dunbarLabel']}")
    print("=======================================================\n")
    
    browser.close()
