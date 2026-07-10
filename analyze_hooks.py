import os
import zipfile
import csv
import io
import re
from datetime import datetime
from collections import defaultdict

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
output_file = r"C:\Users\Antonio\OneDrive\Escritorio\Analisis_Abridores_Comerciales.md"

def parse_linkedin_date(date_str, is_end=False):
    if not date_str or date_str.strip().lower() == "":
        return datetime.now() if is_end else datetime(1970, 1, 1)
    
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }
    
    parts = date_str.strip().split()
    if len(parts) == 2:
        month_str = parts[0][:3].lower()
        year_str = parts[1]
        month = months.get(month_str, 1)
        try:
            year = int(year_str)
            return datetime(year, month, 1)
        except ValueError:
            pass
    elif len(parts) == 1:
        try:
            year = int(parts[0])
            return datetime(year, 12, 31) if is_end else datetime(year, 1, 1)
        except ValueError:
            pass
            
    return datetime.now() if is_end else datetime(1970, 1, 1)

def load_timeline_from_zip():
    timeline = []
    if not os.path.exists(zip_path):
        return timeline
        
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if 'Positions.csv' in zip_ref.namelist():
                with zip_ref.open('Positions.csv') as f:
                    text_file = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                    reader = csv.reader(text_file)
                    header = next(reader)
                    
                    company_idx = header.index('Company Name')
                    title_idx = header.index('Title')
                    start_idx = header.index('Started On')
                    end_idx = header.index('Finished On')
                    
                    for row in reader:
                        if len(row) <= max(company_idx, title_idx, start_idx, end_idx):
                            continue
                        
                        company = row[company_idx].strip()
                        title = row[title_idx].strip()
                        start_str = row[start_idx].strip()
                        end_str = row[end_idx].strip()
                        
                        title_lower = title.lower()
                        is_sales_role = any(kw in title_lower for kw in ["sales", "acquisitions", "bdr", "desarrollo", "comercial", "creador", "consultant", "ventas", "representative", "manager"])
                        
                        if is_sales_role:
                            start_dt = parse_linkedin_date(start_str, is_end=False)
                            end_dt = parse_linkedin_date(end_str, is_end=True)
                            
                            clean_comp = re.sub(r'\s*\(.*\)', '', company).strip()
                            sales_keywords = [clean_comp.lower()]
                            
                            # Add helper words for payment companies
                            if "clip" in clean_comp.lower():
                                sales_keywords.extend(["clip", "terminal", "lector", "tpv", "pagos card", "pos"])
                            elif "fiserv" in clean_comp.lower():
                                sales_keywords.extend(["fiserv", "terminales", "carat", "adquirente", "pos", "cobro"])
                            elif "commerce" in clean_comp.lower() or "latam" in clean_comp.lower():
                                sales_keywords.extend(["commerce", "latam", "odoo", "ecommerce", "tienda"])
                            
                            timeline.append({
                                "company": clean_comp,
                                "start": start_dt,
                                "end": end_dt,
                                "keywords": sales_keywords,
                                "title": title
                            })
                            
        timeline.sort(key=lambda x: x["start"])
        print(f"Loaded {len(timeline)} official sales periods from Positions.csv.")
            
    except Exception as e:
        print(f"Error loading timeline from ZIP: {e}")
        
    return timeline

# Global timeline loaded at runtime
DYNAMIC_TIMELINE = load_timeline_from_zip()

def get_company_by_date(date_str):
    try:
        date_part = date_str[:10]
        msg_date = datetime.strptime(date_part, "%Y-%m-%d")
        
        for period in DYNAMIC_TIMELINE:
            if period["start"] <= msg_date <= period["end"]:
                return period["company"], period["keywords"]
    except Exception as e:
        pass
    
    if DYNAMIC_TIMELINE:
        latest = DYNAMIC_TIMELINE[-1]
        return latest["company"], latest["keywords"]
        
    return "Desconocido", []

def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r'[áéíóúü]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u'}[m.group(0)], text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_user(sender_name):
    norm = normalize_text(sender_name)
    return ("antonio" in norm and "gutierrez" in norm) or "antonio gutierrez" in norm or "tono" in norm or norm == "antonio gutierrez jimenez"

def matches_keyword(content_norm, keyword):
    """
    Checks if keyword matches the normalized content.
    If keyword has spaces, it does substring matching.
    If it is a single word, it does whole-word matching using word boundaries.
    """
    if not keyword:
        return False
    if " " in keyword:
        return keyword in content_norm
    # Use word boundary to avoid partial matches (e.g. 'pos' matching 'posible' or 'posicion')
    pattern = r'\b' + re.escape(keyword) + r'\b'
    return bool(re.search(pattern, content_norm))

def classify_conversation(msgs):
    if not msgs:
        return "Otros / Sin Clasificar"
        
    representative_date = msgs[0]["date"]
    current_sales_company, active_kws = get_company_by_date(representative_date)
    
    has_active_sales_pitch = False
    has_sale_to_me = False
    has_recruitment = False
    has_tech_networking = False
    
    sale_to_me_kws = ["nuestra plataforma", "nuestro servicio", "te presento", "scrabin", "licencia", "demo de", "prueba gratis", "nuestro software", "automatizar", "automatizacion", "mi producto"]
    recruitment_kws = ["cv", "curriculum", "vacante", "puesto", "rol", "entrevista", "contratacion", "reclutador", "reclutamiento", "headhunter", "talento", "salario", "sueldo", "empleo", "oferta laboral"]
    tech_net_kws = ["ayuda", "codigo", "app", "desarrollo", "programacion", "consejo", "opinion", "comparto", "articulo", "post", "github", "api", "framework", "libreria"]

    for msg in msgs:
        content_norm = normalize_text(msg["content"])
        sender_is_me = is_user(msg["sender"])
        
        if sender_is_me:
            if any(matches_keyword(content_norm, kw) for kw in active_kws):
                has_active_sales_pitch = True
        else:
            if any(matches_keyword(content_norm, kw) for kw in sale_to_me_kws):
                has_sale_to_me = True
        
        if any(matches_keyword(content_norm, kw) for kw in recruitment_kws):
            has_recruitment = True
            
        if any(matches_keyword(content_norm, kw) for kw in tech_net_kws):
            has_tech_networking = True

    if has_active_sales_pitch and not has_recruitment:
        return f"Venta para Mí ({current_sales_company})"
    elif has_sale_to_me:
        return "Venta hacia Mí (Me querían vender)"
    elif has_recruitment:
        return "Reclutamiento / Empleo"
    elif has_tech_networking:
        return "Networking Técnico / Ayuda"
    else:
        return "Networking General / Saludos"

def analyze_conversational_hooks():
    if not os.path.exists(zip_path):
        print(f"Zip file not found at: {zip_path}")
        return
        
    global DYNAMIC_TIMELINE
    DYNAMIC_TIMELINE = load_timeline_from_zip()
    
    print("Reading messages.csv from ZIP...")
    conversations = defaultdict(list)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            with zip_ref.open('messages.csv') as f:
                text_file = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(text_file)
                header = next(reader)
                
                conv_id_idx = header.index('CONVERSATION ID')
                from_idx = header.index('FROM')
                to_idx = header.index('TO')
                date_idx = header.index('DATE')
                content_idx = header.index('CONTENT')
                
                for row in reader:
                    if len(row) <= max(conv_id_idx, date_idx, content_idx):
                        continue
                    
                    conv_id = row[conv_id_idx]
                    sender = row[from_idx]
                    recipient = row[to_idx]
                    date = row[date_idx]
                    content = row[content_idx].strip()
                    
                    conversations[conv_id].append({
                        "sender": sender,
                        "recipient": recipient,
                        "date": date,
                        "content": content
                    })
                    
        print(f"Loaded {len(conversations)} conversations.")
        
        openers_stats = []
        
        for conv_id, msgs in conversations.items():
            msgs.sort(key=lambda x: x["date"])
            
            if not msgs:
                continue
                
            first_my_msg_idx = -1
            for idx, msg in enumerate(msgs):
                if is_user(msg["sender"]):
                    first_my_msg_idx = idx
                    break
            
            if first_my_msg_idx == -1:
                continue
                
            opener_msg = msgs[first_my_msg_idx]
            opener_text = opener_msg["content"]
            
            replied = False
            subsequent_msgs = msgs[first_my_msg_idx + 1:]
            total_turns = len(subsequent_msgs)
            
            other_person_name = ""
            for sub_msg in subsequent_msgs:
                if not is_user(sub_msg["sender"]):
                    replied = True
                    other_person_name = sub_msg["sender"]
                    break
            
            conv_type = classify_conversation(msgs)
            
            short_text = opener_text.replace("\n", " ").strip()
            if len(short_text) > 300:
                short_text = short_text[:300] + "..."
            
            openers_stats.append({
                "other_person": other_person_name or "Desconocido",
                "opener_text": short_text,
                "replied": replied,
                "turns": total_turns,
                "type": conv_type
            })
            
        print(f"Analyzed {len(openers_stats)} openers sent by the user.")
        
        type_groups = defaultdict(list)
        for op in openers_stats:
            type_groups[op["type"]].append(op)
            
        my_sales_openers = []
        for key, val in type_groups.items():
            if "Venta para Mí" in key:
                my_sales_openers.extend(val)
        
        categories = {
            "Pregunta / Ayuda Directa": [],
            "Presentación Larga / Propuesta": [],
            "Saludo Simple / Informal": [],
            "Otros / Sin Clasificar": []
        }
        
        for op in my_sales_openers:
            text = normalize_text(op["opener_text"])
            if "como vas" in text or "hola" in text and len(text) < 40:
                categories["Saludo Simple / Informal"].append(op)
            elif any(matches_keyword(text, kw) for kw in ["clip", "fiserv", "latam commerce", "odoo", "terminal", "pagos"]):
                categories["Pregunta / Ayuda Directa"].append(op)
            elif len(text) > 100:
                categories["Presentación Larga / Propuesta"].append(op)
            else:
                categories["Otros / Sin Clasificar"].append(op)
                
        # Generate the Markdown Report
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("# 📡 Análisis de Abridores Comerciales: ¿Qué funciona en tu red?\n\n")
            out.write("Este informe analiza tus mensajes de apertura en LinkedIn DMs, clasificando las relaciones de forma dinámica según tu **Línea de Tiempo Profesional de LinkedIn** (Fiserv, Clip, LATAM Commerce).\n\n")
            
            out.write("## 📊 Distribución de Relaciones en tu Red (Alineada con tu Perfil Oficial)\n")
            out.write("Clasificación de tus conversaciones con base en la empresa en la que trabajabas según tu LinkedIn:\n\n")
            out.write("| Contexto de Conversación | Chats Analizados | Tasa de Respuesta |\n")
            out.write("| :--- | :---: | :---: |\n")
            
            sorted_types = sorted(type_groups.keys(), key=lambda x: ("Venta para Mí" not in x, x))
            for t_name in sorted_types:
                ops = type_groups[t_name]
                t_total = len(ops)
                t_replies = sum(1 for x in ops if x["replied"])
                t_reply_rate = (t_replies / t_total * 100) if t_total else 0
                out.write(f"| **{t_name}** | {t_total} | {t_reply_rate:.1f}% |\n")
                
            out.write("\n---\n\n")
            
            total_sales = len(my_sales_openers)
            sales_replies = sum(1 for x in my_sales_openers if x["replied"])
            sales_reply_rate = (sales_replies / total_sales * 100) if total_sales else 0
            
            out.write("## 🎯 Análisis Exclusivo: Ventas Propias Consolidadas\n")
            out.write(f"Suma de tus campañas comerciales activas en **Clip**, **Fiserv** y **LATAM Commerce**.\n\n")
            out.write(f"- **Mensajes de Apertura de Venta:** `{total_sales}`\n")
            out.write(f"- **Tasa de Respuesta Efectiva:** `{sales_reply_rate:.1f}%` ({sales_replies} respuestas reales)\n\n")
            
            out.write("### 🏆 Rendimiento por Estilo de Abridor (Tus Ventas)\n\n")
            out.write("| Estilo de Abridor | Mensajes | Tasa de Respuesta |\n")
            out.write("| :--- | :---: | :---: |\n")
            
            for cat_name, ops in categories.items():
                cat_total = len(ops)
                if cat_total == 0:
                    continue
                cat_replies = sum(1 for x in ops if x["replied"])
                cat_reply_rate = (cat_replies / cat_total * 100)
                out.write(f"| **{cat_name}** | {cat_total} | {cat_reply_rate:.1f}% |\n")
                
            out.write("\n---\n\n")
            out.write("## 💡 Ejemplos Reales de Conversaciones de Venta por Época\n\n")
            
            # Show top examples of each company period
            for period_company in ["Clip", "Fiserv", "LATAM Commerce"]:
                cat_key = f"Venta para Mí ({period_company})"
                ops_in_cat = sorted([x for x in type_groups[cat_key] if x["replied"] and x["turns"] > 2], key=lambda x: x["turns"], reverse=True)[:3]
                
                if ops_in_cat:
                    out.write(f"### 🚀 Época {period_company}\n")
                    for idx, ex in enumerate(ops_in_cat):
                        out.write(f"#### {idx+1}. Lead: *{ex['other_person']}*\n")
                        out.write(f"- **Tu Abridor Enviado:** \n")
                        out.write(f"  > \"{ex['opener_text']}\"\n")
                        out.write(f"- **Turnos de conversación:** `{ex['turns']}`\n\n")
                
        print(f"Hooks analysis completed successfully. File written to: {output_file}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    analyze_conversational_hooks()
