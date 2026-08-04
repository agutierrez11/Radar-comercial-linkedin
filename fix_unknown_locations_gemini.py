import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

env_path = os.path.join(os.path.dirname(__file__), ".env")
API_KEY = ""
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()

def prompt_gemini(batch_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    prompt = """Eres un experto en inteligencia comercial B2B. 
Se te proporcionará una lista de perfiles profesionales. Cada línea tiene un ID, la Empresa, el Puesto y el Resumen de Google de ese perfil.
Tu objetivo es adivinar el País (Country) con la mayor precisión posible.
Responde ESTRICTAMENTE con un objeto JSON válido donde la clave sea el ID y el valor sea el nombre del País en Español (por ejemplo: "México", "España", "Colombia", "Estados Unidos").
Si es imposible saberlo y no hay indicios de país, devuelve "Desconocido".

Aquí están los perfiles:
""" + batch_text

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1}
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            if "candidates" in res_json and len(res_json["candidates"]) > 0:
                text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                # Limpiar backticks si los hay
                text = text.strip()
                if text.startswith("```json"): text = text[7:]
                if text.startswith("```"): text = text[3:]
                if text.endswith("```"): text = text[:-3]
                
                try:
                    return json.loads(text.strip())
                except json.JSONDecodeError:
                    print("Error decodificando JSON de Gemini. Fragmento:", text[:50])
                    return {}
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("  [!] Rate limit de Gemini. Esperando 15s...")
            time.sleep(15)
            return prompt_gemini(batch_text)
        print("Error HTTP Gemini:", e.code)
    except Exception as e:
        print("Error de red Gemini:", e)
    return {}

def main():
    print("=== INICIANDO RESCATE DE UBICACIONES CON IA (GEMINI 2.5 FLASH) ===")
    
    rows = []
    with open('radar_database_final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
            
    # Filtrar los que necesitan rescate
    to_rescue = []
    for i, row in enumerate(rows):
        if row['Location'] == 'Desconocido' and (row['Company'] or row['Position'] or row['Google Snippet']):
            to_rescue.append((i, row))
            
    print(f"Total perfiles a limpiar con IA: {len(to_rescue)}")
    
    batch_size = 100
    batches = [to_rescue[i:i + batch_size] for i in range(0, len(to_rescue), batch_size)]
    
    print(f"Procesando en {len(batches)} lotes...")
    
    for b_idx, batch in enumerate(batches):
        print(f"-> Batch {b_idx+1}/{len(batches)}...")
        batch_text = ""
        for (idx, row) in batch:
            batch_text += f"ID: {idx} | Empresa: {row['Company']} | Puesto: {row['Position']} | Resumen: {row['Google Snippet']}\n"
            
        results = prompt_gemini(batch_text)
        
        # Actualizar filas
        for idx_str, country in results.items():
            try:
                idx = int(idx_str)
                if country and country != "Desconocido":
                    rows[idx]['Location'] = country
            except:
                pass
        
        # Pequeña pausa anti-spam para la API gratuita
        time.sleep(5)
        
    print("Guardando base de datos final actualizada...")
    with open('radar_database_final.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print("[+] Limpieza con Inteligencia Artificial completada. Base de datos salva.")

if __name__ == "__main__":
    main()
