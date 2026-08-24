import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    print("\n--- TEST 1: MONTHLY REMINDER BANNER RENDERING ---")
    page.goto("http://127.0.0.1:8888/index.html")
    page.wait_for_timeout(1000)
    
    banner_info = page.evaluate("""() => {
      const banner = document.getElementById('monthly-ingestion-reminder-banner');
      return {
        display: banner ? window.getComputedStyle(banner).display : 'NONE',
        text: banner ? banner.textContent : ''
      };
    }""")
    print("Banner info:", banner_info['display'])
    assert banner_info['display'] == 'flex', "Reminder banner must be visible on load"
    assert "Recordatorio de Minería Recurrente" in banner_info['text'], "Banner title verified"
    page.screenshot(path="qa_test4_monthly_reminder_banner.png")
    print("PASSED TEST 1: Reminder banner rendering verified!")

    print("\n--- TEST 2: STEP-BY-STEP MODAL QA ---")
    page.evaluate("openMonthlyIngestionModal();")
    page.wait_for_timeout(500)
    
    modal_info = page.evaluate("""() => {
      const modal = document.getElementById('monthly-ingestion-modal');
      return {
        display: modal ? window.getComputedStyle(modal).display : 'NONE'
      };
    }""")
    print("Modal display:", modal_info['display'])
    assert modal_info['display'] == 'flex', "Monthly ingestion modal must open"
    page.screenshot(path="qa_test5_monthly_reminder_modal.png")
    print("PASSED TEST 2: Step-by-step reminder modal verified!")

    print("\n--- TEST 3: DISMISS & MARK UPDATED QA ---")
    page.evaluate("markVaultUpdatedToday();")
    page.wait_for_timeout(500)
    
    dismiss_info = page.evaluate("""() => {
      const banner = document.getElementById('monthly-ingestion-reminder-banner');
      const modal = document.getElementById('monthly-ingestion-modal');
      const lastIngest = localStorage.getItem('rc_last_csv_ingestion');
      return {
        bannerDisplay: banner ? banner.style.display : 'none',
        modalDisplay: modal ? modal.style.display : 'none',
        hasIngestTimestamp: lastIngest !== null
      };
    }""")
    print("Dismiss info:", dismiss_info)
    assert dismiss_info['bannerDisplay'] == 'none', "Banner must be hidden after marking updated"
    assert dismiss_info['modalDisplay'] == 'none', "Modal must be closed after marking updated"
    assert dismiss_info['hasIngestTimestamp'] == True, "Last CSV ingestion timestamp must be saved"
    page.screenshot(path="qa_test6_monthly_reminder_dismissed.png")
    print("PASSED TEST 3: Dismiss & mark updated verified!")

    browser.close()
    print("\n✅ ALL MONTHLY REMINDER BOT QA TESTS PASSED PERFECTLY!")
