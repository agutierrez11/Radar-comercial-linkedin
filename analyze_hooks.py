import os
import zipfile
import csv
import io
import re
from collections import defaultdict

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
output_file = r"C:\Users\Antonio\OneDrive\Escritorio\Analisis_Abridores_Comerciales.md"

def normalize_text(text):
    text = text.lower().strip()
    # Remove accents
    text = re.sub(r'[áéíóúü]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u'}[m.group(0)], text)
    # Remove emojis and non-alphanumeric/non-space characters
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_user(sender_name):
    norm = normalize_text(sender_name)
    # Check if it contains "antonio gutierrez" or "antonio jimenez" or "tono"
    return ("antonio" in norm and "gutierrez" in norm) or "antonio gutierrez" in norm or "tono" in norm or norm == "antonio gutierrez jimenez"

def analyze_conversational_hooks():
    if not os.path.exists(zip_path):
        print(f"Zip file not found at: {zip_path}")
        return
        
    print("Reading messages.csv from ZIP...")
    
    conversations = defaultdict(list)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            with zip_ref.open('messages.csv') as f:
                text_file = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(text_file)
                header = next(reader)
                
                # Column indices
                conv_id_idx = header.index('CONVERSATION ID')
                conv_title_idx = header.index('CONVERSATION TITLE')
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
        
        commercial_keywords = [
            "reunion", "llamada", "demo", "toku", "netpay", "interesa", "agenda", 
            "platicar", "cita", "zoom", "meet", "telefono", "whatsapp", "cel",
            "oportunidad", "presentar", "colaborar"
        ]
        
        for conv_id, msgs in conversations.items():
            # Sort messages by date
            msgs.sort(key=lambda x: x["date"])
            
            if not msgs:
                continue
                
            # Find the first message sent by Antonio
            first_my_msg_idx = -1
            for idx, msg in enumerate(msgs):
                if is_user(msg["sender"]):
                    first_my_msg_idx = idx
                    break
            
            if first_my_msg_idx == -1:
                continue
                
            opener_msg = msgs[first_my_msg_idx]
            opener_text = opener_msg["content"]
            
            # Did they reply after my opener?
            replied = False
            subsequent_msgs = msgs[first_my_msg_idx + 1:]
            total_turns = len(subsequent_msgs)
            
            other_person_name = ""
            for sub_msg in subsequent_msgs:
                if not is_user(sub_msg["sender"]):
                    replied = True
                    other_person_name = sub_msg["sender"]
                    break
            
            # Check for commercial intent in the conversation
            has_commercial_intent = False
            for msg in msgs:
                text_norm = normalize_text(msg["content"])
                if any(kw in text_norm for kw in commercial_keywords):
                    has_commercial_intent = True
                    break
            
            short_text = opener_text.replace("\n", " ").strip()
            # Truncate clean
            if len(short_text) > 300:
                short_text = short_text[:300] + "..."
            
            openers_stats.append({
                "other_person": other_person_name or "Desconocido",
                "opener_text": short_text,
                "replied": replied,
                "turns": total_turns,
                "commercial": has_commercial_intent
            })
            
        print(f"Analyzed {len(openers_stats)} openers sent by the user.")
        
        categories = {
            "Pregunta / Ayuda Directa": [],
            "Felicidades / Cambio de Puesto": [],
            "Presentación Larga / Propuesta": [],
            "Saludo Simple / Informal": [],
            "Otros / Sin Clasificar": []
        }
        
        for op in openers_stats:
            text = normalize_text(op["opener_text"])
            if "felicidades" in text or "exito" in text or "enhorabuena" in text or "nuevo cargo" in text or "nuevo puesto" in text:
                categories["Felicidades / Cambio de Puesto"].append(op)
            elif "como vas" in text or "hola" in text and len(text) < 40:
                categories["Saludo Simple / Informal"].append(op)
            elif "toku" in text or "netpay" in text or "b2b" in text or "platicar" in text or "reunion" in text or "demo" in text or "agenda" in text:
                categories["Pregunta / Ayuda Directa"].append(op)
            elif len(text) > 100:
                categories["Presentación Larga / Propuesta"].append(op)
            else:
                categories["Otros / Sin Clasificar"].append(op)
                
        # Generate the Markdown Report
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("# 📡 Análisis de Abridores Comerciales: ¿Qué funciona en tu red?\n\n")
            out.write("Este informe analiza semánticamente tus mensajes de apertura históricos en LinkedIn DMs, midiendo la tasa de respuesta y la conversión real a conversaciones comerciales.\n\n")
            
            # High-level metrics
            total_analyzed = len(openers_stats)
            total_replies = sum(1 for x in openers_stats if x["replied"])
            total_commercial = sum(1 for x in openers_stats if x["commercial"])
            
            reply_rate = (total_replies / total_analyzed * 100) if total_analyzed else 0
            commercial_rate = (total_commercial / total_analyzed * 100) if total_analyzed else 0
            
            out.write("## 📊 Métricas Consolidadas de Apertura\n")
            out.write(f"- **Conversaciones Iniciadas por ti:** `{total_analyzed}`\n")
            out.write(f"- **Tasa de Respuesta Global:** `{reply_rate:.1f}%` ({total_replies} respuestas)\n")
            out.write(f"- **Conversiones de Interés Comercial:** `{commercial_rate:.1f}%` ({total_commercial} conversaciones con palabras clave de reunión/demo/interés)\n\n")
            
            out.write("---\n\n")
            out.write("## 🏆 Rendimiento por Categoría de Mensaje\n\n")
            out.write("| Categoría de Abridor | Mensajes Enviados | Tasa de Respuesta | Tasa Conversión Comercial |\n")
            out.write("| :--- | :---: | :---: | :---: |\n")
            
            for cat_name, ops in categories.items():
                cat_total = len(ops)
                if cat_total == 0:
                    continue
                cat_replies = sum(1 for x in ops if x["replied"])
                cat_commercial = sum(1 for x in ops if x["commercial"])
                
                cat_reply_rate = (cat_replies / cat_total * 100)
                cat_comm_rate = (cat_commercial / cat_total * 100)
                
                out.write(f"| **{cat_name}** | {cat_total} | {cat_reply_rate:.1f}% | {cat_comm_rate:.1f}% |\n")
                
            out.write("\n---\n\n")
            out.write("## 💡 Ejemplos de Éxito Comercial (Conversaciones que convirtieron)\n\n")
            
            # Find top 10 commercial conversations that had replies, sorted by number of turns
            successful_examples = sorted([x for x in openers_stats if x["replied"] and x["commercial"]], key=lambda x: x["turns"], reverse=True)[:10]
            
            for idx, ex in enumerate(successful_examples):
                out.write(f"### {idx+1}. Conversación con *{ex['other_person']}*\n")
                out.write(f"- **Abridor enviado:** \n")
                out.write(f"  > \"{ex['opener_text']}\"\n")
                out.write(f"- **Mensajes intercambiados después (Turnos):** `{ex['turns']}`\n\n")
                
        print(f"Hooks analysis completed successfully. File written to: {output_file}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    analyze_conversational_hooks()
