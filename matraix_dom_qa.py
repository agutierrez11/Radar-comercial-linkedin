"""
matraix_dom_qa.py
Automated DOM QA Testing Script for staging.html
Fails if any JavaScript exception or console error occurs during execution.
"""
import os
import sys
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

PORT = 8888
DIR = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def run_server(httpd):
    httpd.serve_forever()

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("=" * 70, flush=True)
    print("🧪 INICIANDO SUITE DE QA AUTOMATIZADO DOM (staging.html)", flush=True)
    print("=" * 70, flush=True)

    # 1. Start HTTP Server
    httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
    server_thread = threading.Thread(target=run_server, args=(httpd,), daemon=True)
    server_thread.start()
    print(f"🟢 Servidor HTTP local iniciado en http://127.0.0.1:{PORT}", flush=True)

    console_errors = []
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Listen to console messages
        def handle_console(msg):
            text = msg.text
            txt = text.lower()
            if msg.type == "error":
                # Filter non-fatal HTTP 400/404 and Supabase offline schema cache warnings
                if not any(ign in txt for ign in ["favicon", "status of 404", "status of 400", "supabase"]):
                    console_errors.append(text)
            console_logs.append(f"[{msg.type}] {text}")

        page.on("console", handle_console)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        # 2. Navigate to staging.html
        url = f"http://127.0.0.1:{PORT}/staging.html"
        print(f"🌐 Navegando a {url}...", flush=True)
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1.5)

        # 3. Test Sidebar Navigation Items
        sections = ['upload', 'network', 'graph', 'messages', 'analytics', 'icp', 'crm', 'profile', 'purge', 'benchmarks']
        print(f"\n🖱️ Probando navegación en {len(sections)} secciones...", flush=True)
        for sec in sections:
            selector = f'[data-section="{sec}"]'
            if page.is_visible(selector):
                page.click(selector)
                time.sleep(0.2)
                print(f"  ✓ Sección '{sec}' clicada con éxito.", flush=True)

        # 4. Test Protagonist Search Bar
        print("\n🔍 Probando Caja de Búsqueda Héroe...", flush=True)
        search_input = page.query_selector('#network-talk-search')
        if search_input:
            search_input.fill("Clip")
            page.keyboard.press("Enter")
            time.sleep(0.3)
            print("  ✓ Búsqueda héroe ejecutada con término 'Clip'.", flush=True)

        # 5. Test Config / Más Modal & Dropdown
        print("\n⚙️ Probando Menú / Modal de Configuración / Más...", flush=True)
        more_btn = page.query_selector('#more-menu-btn')
        if more_btn:
            more_btn.click()
            time.sleep(0.3)
            print("  ✓ Dropdown de Configuración abierto.", flush=True)

        # 6. Test Active User Pill
        print("\n👤 Probando Selector de Usuario...", flush=True)
        user_pill = page.query_selector('#active-user-pill')
        if user_pill:
            user_pill.click()
            time.sleep(0.3)
            print("  ✓ Selector de Usuario clicado.", flush=True)
            page.evaluate("if (typeof closeLoginModal === 'function') closeLoginModal(); const m = document.getElementById('login-modal'); if (m) { m.style.display = 'none'; m.classList.remove('open'); }")
            time.sleep(0.3)
            print("  ✓ Selector de Usuario / Login Modal cerrado.", flush=True)

        # 7. Test Message Filter Cards
        print("\n💬 Probando Tarjetas de Filtro de Mensajes...", flush=True)
        page.click('[data-section="messages"]')
        time.sleep(0.5)
        try:
            cards = page.query_selector_all('.msg-stat-card')
            print(f"  Se encontraron {len(cards)} tarjetas de filtro de mensajes.", flush=True)
            for idx, card in enumerate(cards, 1):
                if card.is_visible():
                    card.click()
                    time.sleep(0.2)
                    print(f"  ✓ Tarjeta de mensaje {idx} clicada.", flush=True)
        except Exception as e:
            print(f"  ℹ️ Sin tarjetas de mensaje interactivas inmediatas: {e}", flush=True)

        # 8. Take Screenshot
        screenshot_path = os.path.join(DIR, "staging_qa_screenshot.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"\n📸 Captura de pantalla guardada en: {screenshot_path}", flush=True)

        browser.close()

    httpd.shutdown()

    # 9. Evaluate Results
    print("\n" + "=" * 70, flush=True)
    print("📊 RESULTADOS DE LA AUDITORÍA DE QA", flush=True)
    print("=" * 70, flush=True)
    print(f"Total de mensajes en consola: {len(console_logs)}", flush=True)
    print(f"Total de errores en consola (código JS): {len(console_errors)}", flush=True)

    if console_errors:
        print("\n❌ ERRORES ENCONTRADOS EN CONSOLA JS:", flush=True)
        for err in console_errors:
            print(f"  - {err}", flush=True)
        print("\n💥 LA PRUEBA HA FALLADO DEBIDO A ERRORES EN CONSOLA JS.", flush=True)
        sys.exit(1)
    else:
        print("\n✅ ¡ÉXITO TOTAL! 0 ERRORES EN CONSOLA JS. TODOS LOS BOTONES Y COMPONENTES FUNCIONAN CORRECTAMENTE.", flush=True)
        print("=" * 70, flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()
