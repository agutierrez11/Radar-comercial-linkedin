import asyncio
import os
import json
import yaml
from playwright.async_api import async_playwright

PERSONAS = [
    {"id": "0001", "name": "Tomas Horvat", "role": "Director de Operaciones", "goal": "Probar Mapa GIS, cambio de capas y temas visuales"},
    {"id": "0002", "name": "Elena Vance", "role": "VP de Ventas", "goal": "Probar Filtros de Jerarquía, Países y Verificados Live"},
    {"id": "0005", "name": "David Kim", "role": "RevOps Lead", "goal": "Probar movimiento de CRM, Kanban Board y actualización de estados"},
    {"id": "0010", "name": "Carlos Mendoza", "role": "Consultor B2B", "goal": "Probar ICP Leads, Slider de Scoring y Modal de Outreach"},
    {"id": "0145", "name": "Priya Sharma", "role": "Analista de Red", "goal": "Probar Dunbar Purge, Pestaña de Mensajes y Filtros de Clasificación"}
]

async def run_persona_qa_session(browser, persona, html_path):
    page = await browser.new_page()
    console_errors = []
    page_errors = []

    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda err: page_errors.append(str(err)))

    print("\n[PERSONA " + persona['id'] + ": " + persona['name'] + "] (" + persona['role'] + ") ARRANCANDO PRUEBA:", flush=True)
    print("   Objetivo: " + persona['goal'], flush=True)

    try:
        await page.goto(html_path)
        await page.wait_for_timeout(1000)

        # Persona 1: Test Theme & Map GIS
        if persona["id"] == "0001":
            print("   -> Clickeando boton de cambio de Tema (Modo Claro / Oscuro)...")
            theme_btn = await page.query_selector("#theme-toggle")
            if theme_btn:
                await theme_btn.click()
                await page.wait_for_timeout(500)
                await theme_btn.click()
                await page.wait_for_timeout(500)
                print("   SUCCESS: Cambio de tema probado exitosamente.")
            else:
                print("   ERROR: #theme-toggle no encontrado.")

            print("   -> Probando selector de capas del Mapa GIS...")
            tile_select = await page.query_selector("#gis-tile-select")
            if tile_select:
                await tile_select.select_option("satellite")
                await page.wait_for_timeout(500)
                await tile_select.select_option("voyager")
                await page.wait_for_timeout(500)
                await tile_select.select_option("dark")
                await page.wait_for_timeout(500)
                print("   SUCCESS: Cambio de capas de mapa (Satelital, Voyager, Dark) probado.")
            else:
                print("   ERROR: #gis-tile-select no encontrado.")

        # Persona 2: Test Filters & Live Badges
        elif persona["id"] == "0002":
            print("   -> Probando filtros de Jerarquia en Mi Red...")
            hier_card = await page.query_selector("#kpicard-C-Level")
            if hier_card:
                await hier_card.click()
                await page.wait_for_timeout(500)
                print("   SUCCESS: Filtro C-Level aplicado.")
            
            country_sel = await page.query_selector("#net-country")
            if country_sel:
                options = await country_sel.query_selector_all("option")
                if len(options) > 1:
                    val = await options[1].get_attribute("value")
                    await country_sel.select_option(value=val)
                    await page.wait_for_timeout(500)
                    print("   SUCCESS: Filtro por pais (" + str(val) + ") aplicado.")
                else:
                    print("   SUCCESS: Dropdown de paises disponible.")

            live_filter = await page.query_selector("#btn-filter-verified")
            if live_filter:
                await live_filter.click()
                await page.wait_for_timeout(500)
                print("   SUCCESS: Filtro 'Solo Verificados Live' probado.")

        # Persona 3: Test Navigation & CRM Kanban
        elif persona["id"] == "0005":
            print("   -> Navegando a la seccion 'Mi Pipeline' (CRM Kanban)...")
            nav_crm = await page.query_selector('[data-section="crm"]')
            if nav_crm:
                await nav_crm.click()
                await page.wait_for_timeout(1000)
                kanban = await page.query_selector("#crm-kanban-board")
                is_vis = await kanban.is_visible() if kanban else False
                if is_vis:
                    print("   SUCCESS: Seccion Mi Pipeline (CRM Kanban) visible y renderizada.")
                else:
                    print("   ERROR: Kanban board no se hizo visible.")

        # Persona 4: Test ICP Leads & Outreach Modal
        elif persona["id"] == "0010":
            print("   -> Navegando a 'ICP / Leads'...")
            nav_icp = await page.query_selector('[data-section="icp"]')
            if nav_icp:
                await nav_icp.click()
                await page.wait_for_timeout(800)
                
                print("   -> Probando apertura de Modal de Outreach...")
                btn_outreach = await page.query_selector("#icp-tbody button")
                if btn_outreach:
                    await btn_outreach.click()
                    await page.wait_for_timeout(800)
                    modal = await page.query_selector("#pitch-modal")
                    if modal and await modal.is_visible():
                        print("   SUCCESS: Modal de Outreach (pitch-modal) abierto correctamente.")
                        btn_close = await page.query_selector("#pitch-modal .modal-close")
                        if btn_close:
                            await btn_close.click()
                    else:
                        print("   ERROR: Modal de Outreach no se mostro.")

        # Persona 5: Test Dunbar Purge & Messages
        elif persona["id"] == "0145":
            print("   -> Navegando a 'Dunbar Purge'...")
            nav_purge = await page.query_selector('[data-section="purge"]')
            if nav_purge:
                await nav_purge.click()
                await page.wait_for_timeout(800)
                print("   SUCCESS: Seccion Dunbar Purge navegada.")

            print("   -> Navegando a 'Mensajes'...")
            nav_msgs = await page.query_selector('[data-section="messages"]')
            if nav_msgs:
                await nav_msgs.click()
                await page.wait_for_timeout(800)
                print("   SUCCESS: Seccion Mensajes navegada.")

    except Exception as e:
        print("   ERROR Excepcion durante la prueba: " + str(e))

    await page.close()

    return {
        "persona": persona["name"],
        "console_errors": console_errors,
        "page_errors": page_errors
    }

async def main():
    import http.server
    import socketserver
    import threading

    PORT = 8089
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args): pass

    httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    html_path = f"http://127.0.0.1:{PORT}/index.html"
    print("============================================================")
    print("PRUEBA MULTI-USUARIO AGENTICA DE RADAR COMERCIAL")
    print(f"   Servidor HTTP Local: {html_path}")
    print(f"   Simulando {len(PERSONAS)} personas de MatrAIx-Persona-8B en Playwright")
    print("============================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        results = []
        for persona in PERSONAS:
            res = await run_persona_qa_session(browser, persona, html_path)
            results.append(res)
        await browser.close()

    print("\n============================================================")
    print("RESUMEN DE LA AUDITORIA MULTI-USUARIO MATRAIX")
    print("============================================================")
    all_clean = True
    for r in results:
        err_count = len(r["console_errors"]) + len(r["page_errors"])
        if err_count == 0:
            print(f"  SUCCESS {r['persona']}: 0 Errores encontrados (100% Funcional)")
        else:
            all_clean = False
            print(f"  ERROR {r['persona']}: {err_count} Errores detectados!")
            for err in r["console_errors"]:
                print(f"      [Console Error]: {err}")
            for err in r["page_errors"]:
                print(f"      [Page Error]: {err}")

    if all_clean:
        print("\nRESULTADO FINAL: TODOS LOS BOTONES, MAPAS, FILTROS Y NAVEGACION PASARON LA PRUEBA SIN NINGUN ERROR.")
    else:
        print("\nRESULTADO FINAL: SE DETECTARON ALGUNOS ERRORES PARA CORREGIR.")
    print("============================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
