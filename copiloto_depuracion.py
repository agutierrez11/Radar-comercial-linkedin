import os
import csv
import json
import webbrowser
import sys
import pyperclip
import urllib.request
import urllib.parse
from datetime import datetime

# Configurar consola para usar UTF-8 en Windows
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de archivos
env_path = os.path.join(os.path.dirname(__file__), ".env")
connections_file = os.path.join(os.path.dirname(__file__), "connections_to_purge.csv")
progress_file = os.path.join(os.path.dirname(__file__), "depuracion_progreso.json")

def load_env():
    """Reads local .env file without external dependencies."""
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def parse_date(date_str):
    # Formato: "04 Jul 2026"
    try:
        return datetime.strptime(date_str.strip(), "%d %b %Y")
    except Exception:
        return None

def load_progress():
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "deleted_urls": [],
        "kept_urls": []
    }

def save_progress(progress):
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def generar_mensaje_gemini(first_name, last_name, company, position, gemini_key):
    prompt = f"""
    Eres un asistente de ventas de alta calidad. Redacta un mensaje de LinkedIn corto, informal, natural y cálido en español para reactivar el contacto con un ex-colega o conexión profesional antigua.

    Datos del contacto:
    - Nombre: {first_name} {last_name}
    - Cargo: {position}
    - Empresa: {company}

    Tus datos (Antonio):
    - Recientemente te convertiste en papá.
    - Estás en busca de nuevas oportunidades y trabajando en proyectos freelance en medios de pago, adquirencia y e-commerce.

    Directrices del mensaje:
    1. Comienza saludando de forma de chat informal (ej. "Hola {first_name}").
    2. Menciona que llevan conectados un tiempo por aquí pero no han tenido oportunidad de platicar.
    3. Haz referencia a su cargo ("{position}") o su empresa ("{company}") de manera muy natural e integrada, felicitándole o mostrando interés genuino (evita sonar robótico, sé humano).
    4. Comparte de forma breve y amigable tus dos noticias de forma fluida (lo de ser papá y tus proyectos independientes en pagos/e-commerce).
    5. Termina con una pregunta abierta blanda para abrir la conversación (por ejemplo, preguntarle en qué proyectos anda él ahora).
    6. Tono: Cercano, humano, dinámico (como si le escribieras a un colega, evita lenguaje comercial genérico o plantillas rígidas).
    7. Extensión máxima: 120 palabras.
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            text = res_json["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()
    except Exception as e:
        print(f"      [!] Error llamando a la API de Gemini: {e}")
        return None

def main():
    print("=========================================================")
    print("   COPILOTO DE DEPURACIÓN MANUAL DE LINKEDIN (RIESGO 0)  ")
    print("=========================================================")
    print("Este script te guiará para eliminar conexiones viejas e inactivas")
    print("de forma manual y segura en tu navegador Chrome habitual.\n")
    
    # Cargar variables de entorno (Gemini Key)
    env_vars = load_env()
    gemini_key = env_vars.get("GEMINI_API_KEY")
    if not gemini_key:
        print("[!] Nota: GEMINI_API_KEY no configurada en .env. El script usará mensajes por defecto.")
        print("    Si quieres mensajes personalizados con IA, puedes agregar tu clave a tu .env.\n")
    
    # 1. Cargar las conexiones auditadas por Apify
    audited_file = os.path.join(os.path.dirname(__file__), "audited_connections.csv")
    
    if not os.path.exists(audited_file):
        print("[!] ADVERTENCIA: No se encontró el archivo audited_connections.csv.")
        print("    Para usar este copiloto inteligente, primero debes ejecutar la auditoría con Apify:")
        print("    run -> python audit_apify_batch.py")
        print("    Este script leerá ese reporte y te guiará para eliminar únicamente a los inactivos.")
        return
        
    candidates = []
    
    try:
        with open(audited_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filtrar conexiones antiguas de 2017-2022
                conn_date = parse_date(row["Connected On"])
                if conn_date and conn_date.year in [2017, 2018, 2019, 2020, 2021, 2022]:
                    # Filtrar únicamente a los confirmados como INACTIVOS por Apify
                    if row["Audit Status"] == "Inactivo":
                        candidates.append({
                            "first_name": row["First Name"],
                            "last_name": row["Last Name"],
                            "url": row["URL"],
                            "company": row["Company"],
                            "position": row["Position"],
                            "connected_on": row["Connected On"],
                            "last_post_date": row["Last Post Date"]
                        })
    except Exception as e:
        print(f"[!] Error leyendo audited_connections.csv: {e}")
        return

    # Ordenar por fecha de conexión (más antiguos primero)
    candidates.sort(key=lambda x: parse_date(x["connected_on"]) if parse_date(x["connected_on"]) else datetime.min)
    
    total_candidates = len(candidates)
    print(f"[+] Se encontraron {total_candidates} contactos confirmados como INACTIVOS por Apify (años 2017-2022).")
    
    if total_candidates == 0:
        print("¡Excelente! No se encontraron contactos inactivos en este rango.")
        return


    # 4. Cargar progreso
    progress = load_progress()
    deleted_urls = set(progress["deleted_urls"])
    kept_urls = set(progress["kept_urls"])
    
    # Filtrar candidatos ya procesados
    pending = [c for c in candidates if c["url"].strip().lower() not in deleted_urls and c["url"].strip().lower() not in kept_urls]
    
    print(f"[+] Ya has procesado {len(deleted_urls) + len(kept_urls)} contactos.")
    print(f"[+] Quedan {len(pending)} contactos pendientes por revisar.")
    
    if not pending:
        print("\n¡Excelente! Has revisado todas las conexiones mudas de 2017-2022.")
        return

    print("\nINSTRUCCIONES DE USO:")
    print("1. El script abrirá el perfil del contacto en tu navegador habitual.")
    print("2. En LinkedIn, haz clic en el botón 'Más' (More) en su perfil -> 'Eliminar contacto' (Remove connection).")
    print("3. Regresa a esta terminal y selecciona una opción:")
    print("   [Enter] = Confirmar que lo eliminaste.")
    print("   [s]     = Saltar (conservar este contacto).")
    print("   [q]     = Guardar progreso y Salir.")
    print("-" * 60)
    
    input("\nPresiona Enter para comenzar...")

    for idx, c in enumerate(pending, 1):
        url_clean = c["url"].strip().lower()
        print(f"\n[{idx}/{len(pending)}] revisando: {c['first_name']} {c['last_name']}")
        print(f"  * Empresa: {c['company']}")
        print(f"  * Cargo:   {c['position']}")
        print(f"  * Conexión: {c['connected_on']}")
        print(f"  * Enlace:   {c['url']}")
        
        # Copiar URL al portapapeles por comodidad
        pyperclip.copy(c["url"])
        
        # Abrir en el navegador predeterminado
        try:
            webbrowser.open(c["url"])
            print("  [✓] Perfil abierto en navegador (URL copiada al portapapeles)")
        except Exception as e:
            print(f"  [!] No se pudo abrir automáticamente el navegador: {e}")
            
        # Esperar feedback del usuario
        while True:
            choice = input("Acción ([Enter] Borrar, [s] Saltar/Conservar, [m] Reactivar/Mensaje, [q] Guardar y Salir): ").strip().lower()
            
            if choice == "":
                # Confirmó eliminación
                progress["deleted_urls"].append(url_clean)
                print(f"  [x] Marcado como ELIMINADO de tu red.")
                break
            elif choice == "s":
                # Decidió conservar sin escribir
                progress["kept_urls"].append(url_clean)
                print(f"  [+] Marcado como CONSERVADO (sin mensaje).")
                break
            elif choice == "m":
                # Decidió conservar y enviarle mensaje de reactivación
                first_name = c["first_name"].strip()
                last_name = c["last_name"].strip()
                company = c["company"].strip()
                position = c["position"].strip()
                
                mensaje = None
                if gemini_key:
                    print("  [🤖] Generando mensaje hiper-personalizado con Gemini...")
                    mensaje = generar_mensaje_gemini(first_name, last_name, company, position, gemini_key)
                
                # Fallback al mensaje por defecto
                if not mensaje:
                    mensaje = (
                        f"Hola {first_name}, qué gusto saludarte. Conectamos hace tiempo por aquí "
                        f"pero realmente no habíamos tenido la oportunidad de platicar. \n\n"
                        f"Te escribo rápido para saludarte y hacer un breve catch up. Por mi lado te comparto "
                        f"que recientemente me convertí en papá y profesionalmente estoy en busca de nuevas oportunidades, "
                        f"colaborando además en proyectos freelance especializados en medios de pago, adquirencia y e-commerce. \n\n"
                        f"¿Cómo te ha ido a ti últimamente? ¿En qué proyectos andas metido ahora?\n\n"
                        f"¡Un abrazo!"
                    )
                
                pyperclip.copy(mensaje)
                progress["kept_urls"].append(url_clean)
                print(f"  [✉] ¡Mensaje personalizado copiado al portapapeles!")
                print(f"      Mensaje generado:\n{'-'*40}\n{mensaje}\n{'-'*40}")
                print(f"      Pégalo en el chat de LinkedIn (Ctrl + V). Marcado como CONSERVADO.")
                break

            elif choice == "q":
                # Salir
                save_progress(progress)
                print(f"\n[!] Progreso guardado. Has procesado {idx-1} contactos en esta sesión.")
                print("¡Hasta pronto!")
                return
            else:
                print("Opción no válida. Escribe 's', 'm', 'q' o presiona [Enter].")
                
        # Guardar progreso en cada paso
        save_progress(progress)


    print("\n¡Felicidades! Has terminado de revisar todo el listado de conexiones mudas de 2017-2022.")

if __name__ == "__main__":
    main()
