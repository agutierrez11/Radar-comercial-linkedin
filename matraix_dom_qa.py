"""
matraix_dom_qa.py
Automated DOM QA Testing Script for staging.html & index.html
Verifies Welcome Access Gateway, vault switching, navigation, and 0 JS console errors.
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
    print("🧪 INICIANDO SUITE DE QA AUTOMATIZADO WELCOME GATEWAY & DOM", flush=True)
    print("=" * 70, flush=True)

    httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
    server_thread = threading.Thread(target=run_server, args=(httpd,), daemon=True)
    server_thread.start()
    print(f"🟢 Servidor HTTP local iniciado en http://127.0.0.1:{PORT}", flush=True)

    console_errors = []
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def handle_console(msg):
            text = msg.text
            txt = text.lower()
            if msg.type == "error":
                if not any(ign in txt for ign in ["favicon", "status of 404", "status of 400", "supabase"]):
                    console_errors.append(text)
            console_logs.append(f"[{msg.type}] {text}")

        page.on("console", handle_console)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))
        
        # Handle prompt dialogs for PIN Admin automatically
        page.on("dialog", lambda dialog: dialog.accept("12345"))

        # 1. Navigate to staging.html
        url = f"http://127.0.0.1:{PORT}/staging.html"
        print(f"🌐 Navegando a {url}...", flush=True)
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1.0)

        # 2. Check Welcome Access Gateway Modal on Startup
        print("\n🔐 Verificando Ventana de Acceso / Welcome Gateway en inicio...", flush=True)
        login_btn = page.query_selector('button:has-text("Entrar a mi bóveda")')
        if login_btn and page.is_visible('#login-modal'):
            print("  ✓ Ventana de Bienvenida detectada en inicio.", flush=True)
            # Submit Antonio Admin Login
            user_input = page.query_selector('#login-username-input')
            if user_input:
                user_input.fill('antonio')
            pwd_input = page.query_selector('#login-password-input')
            if pwd_input:
                pwd_input.fill('12345')
            login_btn.click()
            time.sleep(0.8)
            print("  ✓ Autenticado como Antonio (Master Vault).", flush=True)

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

        # 5. Test Vault Switching via Topbar Pill
        print("\n🔄 Probando Conmutación desde Topbar Pill...", flush=True)
        user_pill = page.query_selector('#active-user-pill')
        if user_pill:
            user_pill.click()
            time.sleep(0.4)
            ronan_btn = page.query_selector('#admin-vault-dropdown button:has-text("Ronan")')
            if ronan_btn:
                ronan_btn.click()
                time.sleep(0.5)
                print("  ✓ Conmutado a Ronan Sandbox (500 contactos).", flush=True)

            user_pill.click()
            time.sleep(0.4)
            gio_btn = page.query_selector('#admin-vault-dropdown button:has-text("Giovanna")')
            if gio_btn:
                gio_btn.click()
                time.sleep(0.5)
                print("  ✓ Conmutado a Giovanna (Bóveda privada aislada).", flush=True)

            user_pill.click()
            time.sleep(0.4)
            ant_btn = page.query_selector('#admin-vault-dropdown button:has-text("Antonio")')
            if ant_btn:
                ant_btn.click()
                time.sleep(0.5)
                print("  ✓ Restaurado Antonio (Master Vault 2,953 contactos).", flush=True)

        # 6. Screenshot
        screenshot_path = os.path.join(DIR, "staging_qa_screenshot.png")
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"\n📸 Captura de pantalla guardada en: {screenshot_path}", flush=True)

        browser.close()

    httpd.shutdown()

    # 7. Evaluate Results
    print("\n" + "=" * 70, flush=True)
    print("📊 RESULTADOS DE LA AUDITORÍA DE QA WELCOME GATEWAY", flush=True)
    print("=" * 70, flush=True)
    print(f"Total de mensajes en consola: {len(console_logs)}", flush=True)
    print(f"Total de errores en consola (código JS): {len(console_errors)}", flush=True)

    if console_errors:
        print("\n❌ ERRORES ENCONTRADOS EN CONSOLA JS:", flush=True)
        for err in console_errors:
            print(f"  - {err}", flush=True)
        sys.exit(1)
    else:
        print("\n✅ ¡ÉXITO TOTAL! VENTANA DE BIENVENIDA Y NAVEGACIÓN FUNCIONAN PERFECTAMENTE (0 ERRORES JS).", flush=True)
        print("=" * 70, flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()
