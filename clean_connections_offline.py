import zipfile
import csv
import io
import sys
import re
from datetime import datetime

# Configurar stdout para usar UTF-8 y evitar errores de encoding en Windows
sys.stdout.reconfigure(encoding='utf-8')

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

def parse_date(date_str):
    # Formatos típicos de LinkedIn: "04 Jul 2026" o "2026-07-04 12:34:56"
    date_str = date_str.strip()
    if not date_str:
        return None
    
    # Intentar formato "04 Jul 2026"
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except ValueError:
        pass
    
    # Intentar formato "YYYY-MM-DD HH:MM:SS" (común en mensajes)
    try:
        # Cortar a YYYY-MM-DD
        short_date = date_str.split()[0]
        return datetime.strptime(short_date, "%Y-%m-%d")
    except ValueError:
        pass
        
    return None

def clean_linkedin_url(url):
    if not url:
        return ""
    # Quitar parámetros de búsqueda o barras finales
    url = url.strip().lower()
    url = re.sub(r'\?.*$', '', url)
    url = url.rstrip('/')
    return url

def main():
    connections = {}
    
    print("1. Cargando conexiones de Connections.csv...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            if 'Connections.csv' not in z.namelist():
                print("Error: Connections.csv no encontrado en el ZIP.")
                return
                
            with z.open('Connections.csv') as f:
                # Wrap bytes a text stream con utf-8
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                
                # Saltar las notas iniciales de LinkedIn hasta encontrar el header real
                header = None
                for row in reader:
                    if len(row) > 0 and 'First Name' in row:
                        header = row
                        break
                
                if not header:
                    print("Error: No se pudo encontrar el encabezado real de Connections.csv.")
                    return
                
                # Leer las conexiones
                for row in reader:
                    if len(row) < 7:
                        continue
                    first_name = row[0]
                    last_name = row[1]
                    url = clean_linkedin_url(row[2])
                    email = row[3]
                    company = row[4]
                    position = row[5]
                    connected_on_str = row[6]
                    
                    if not url:
                        continue
                        
                    connected_on = parse_date(connected_on_str)
                    
                    connections[url] = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "company": company,
                        "position": position,
                        "connected_on": connected_on,
                        "connected_on_str": connected_on_str,
                        "message_count": 0,
                        "last_message_date": None,
                        "last_message_content": ""
                    }
        print(f"   Se cargaron {len(connections)} conexiones.")
    except Exception as e:
        print(f"Error procesando Connections.csv: {e}")
        return

    print("\n2. Analizando historial de mensajes (messages.csv)...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            if 'messages.csv' not in z.namelist():
                print("Error: messages.csv no encontrado en el ZIP.")
                return
                
            with z.open('messages.csv') as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                header = next(reader)
                
                # Mapear índices
                try:
                    sender_idx = header.index("SENDER PROFILE URL")
                    recipients_idx = header.index("RECIPIENT PROFILE URLS")
                    date_idx = header.index("DATE")
                    content_idx = header.index("CONTENT")
                except ValueError as ve:
                    print(f"Error en estructura de messages.csv: {ve}")
                    return
                
                processed_messages = 0
                for row in reader:
                    if len(row) <= max(sender_idx, recipients_idx, date_idx, content_idx):
                        continue
                        
                    sender_url = clean_linkedin_url(row[sender_idx])
                    recipients_str = row[recipients_idx]
                    date_str = row[date_idx]
                    content = row[content_idx]
                    
                    msg_date = parse_date(date_str)
                    
                    # Extraer todas las URLs de destinatarios
                    recipient_urls = [clean_linkedin_url(u) for u in re.findall(r'https?://[^\s,\"]+', recipients_str)]
                    
                    # 1. Si tú eres el emisor, registrar interacción en los destinatarios
                    for r_url in recipient_urls:
                        if r_url in connections:
                            connections[r_url]["message_count"] += 1
                            if not connections[r_url]["last_message_date"] or (msg_date and msg_date > connections[r_url]["last_message_date"]):
                                connections[r_url]["last_message_date"] = msg_date
                                connections[r_url]["last_message_content"] = content[:100]
                    
                    # 2. Si el emisor es uno de tus contactos, registrar interacción
                    if sender_url in connections:
                        connections[sender_url]["message_count"] += 1
                        if not connections[sender_url]["last_message_date"] or (msg_date and msg_date > connections[sender_url]["last_message_date"]):
                            connections[sender_url]["last_message_date"] = msg_date
                            connections[sender_url]["last_message_content"] = content[:100]
                            
                    processed_messages += 1
                    
        print(f"   Se procesaron {processed_messages} mensajes.")
    except Exception as e:
        print(f"Error procesando messages.csv: {e}")
        return

    # 3. Clasificar y generar reportes
    print("\n3. Generando reportes...")
    
    total_conns = len(connections)
    chatted_conns = 0
    never_chatted = 0
    
    never_chatted_by_year = {}
    
    # Listas para exportar
    keep_list = []
    purge_list = []
    
    for url, data in connections.items():
        if data["message_count"] > 0:
            chatted_conns += 1
            keep_list.append(data)
        else:
            never_chatted += 1
            purge_list.append(data)
            
            # Agrupar por año de conexión para saber la antigüedad del silencio
            if data["connected_on"]:
                year = data["connected_on"].year
                never_chatted_by_year[year] = never_chatted_by_year.get(year, 0) + 1
            else:
                never_chatted_by_year["Desconocido"] = never_chatted_by_year.get("Desconocido", 0) + 1

    # Ordenar las listas
    # Keep_list ordenada por número de mensajes (descendente)
    keep_list.sort(key=lambda x: x["message_count"], reverse=True)
    # Purge_list ordenada por fecha de conexión (más antigua primero)
    purge_list.sort(key=lambda x: x["connected_on"] if x["connected_on"] else datetime.min)

    # Escribir auditoría detallada
    audit_file = "connections_audit.txt"
    with open(audit_file, "w", encoding="utf-8") as out:
        out.write("==================================================\n")
        out.write("     AUDITORÍA OFFLINE DE CONEXIONES DE LINKEDIN  \n")
        out.write("==================================================\n\n")
        out.write(f"Fecha de Auditoría: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Total de conexiones analizadas: {total_conns}\n\n")
        
        out.write("ESTADÍSTICAS CLAVE:\n")
        out.write(f"- Conexiones con las que HAS CHATEADO (al menos 1 mensaje): {chatted_conns} ({chatted_conns/total_conns*100:.1f}%)\n")
        out.write(f"- Conexiones con las que NUNCA HAS CHATEADO (0 mensajes): {never_chatted} ({never_chatted/total_conns*100:.1f}%)\n\n")
        
        out.write("ANTIGÜEDAD DE CONEXIONES CON LAS QUE NUNCA HAS HABLADO (0 Mensajes):\n")
        for year in sorted(never_chatted_by_year.keys(), key=lambda x: int(x) if isinstance(x, int) else 9999):
            count = never_chatted_by_year[year]
            out.write(f"  * Año {year}: {count} contactos\n")
            
        out.write("\n==================================================\n")
        out.write("TOP 30 CONEXIONES CON MAYOR INTERACCIÓN (Mensajes):\n")
        out.write("==================================================\n")
        for idx, conn in enumerate(keep_list[:30], 1):
            last_msg_str = conn["last_message_date"].strftime('%Y-%m-%d') if conn["last_message_date"] else "N/A"
            out.write(f"{idx}. {conn['first_name']} {conn['last_name']} ({conn['company']} - {conn['position']})\n")
            out.write(f"   Mensajes: {conn['message_count']} | Último: {last_msg_str}\n")
            out.write(f"   Último fragmento: \"{conn['last_message_content']}\"\n\n")
            
        out.write("\n==================================================\n")
        out.write("TOP 50 CONEXIONES ANTIGUAS SIN INTERACCIÓN (Candidatos a Purga):\n")
        out.write("==================================================\n")
        for idx, conn in enumerate(purge_list[:50], 1):
            out.write(f"{idx}. {conn['first_name']} {conn['last_name']} | Conectado el: {conn['connected_on_str']}\n")
            out.write(f"   Empresa: {conn['company']} | Cargo: {conn['position']}\n\n")

    # Guardar CSV de depuración
    with open("connections_to_purge.csv", "w", newline="", encoding="utf-8") as f_purge:
        writer = csv.writer(f_purge)
        writer.writerow(["First Name", "Last Name", "Connected On", "Company", "Position", "Email"])
        for conn in purge_list:
            writer.writerow([conn["first_name"], conn["last_name"], conn["connected_on_str"], conn["company"], conn["position"], conn["email"]])
            
    print(f"\n¡Completado!")
    print(f"- Auditoría detallada escrita en: {audit_file}")
    print(f"- Lista de candidatos a eliminar ({len(purge_list)} contactos) exportada a: connections_to_purge.csv")

if __name__ == "__main__":
    main()
