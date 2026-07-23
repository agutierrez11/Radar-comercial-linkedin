import csv
import json
import os
import sys
import time

# Forzar UTF-8 en stdout para Windows
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("\n[!] ERROR: ANTHROPIC_API_KEY no encontrada.")
    sys.exit(1)

import anthropic
client = anthropic.Anthropic(api_key=api_key)

csv_path = "audited_connections.csv"
output_path = "locations_normalized.json"

def get_unique_strings():
    unique_strings = set()
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get("Company", "").strip()
                position = row.get("Position", "").strip()
                if company or position:
                    unique_strings.add(f"{company} | {position}")
    except FileNotFoundError:
        print(f"Error: No se encontró {csv_path}")
        sys.exit(1)
    return list(unique_strings)

def normalize_batch(batch):
    prompt = """Eres un experto en normalización de datos geográficos para un CRM B2B.
Analiza la siguiente lista de strings que tienen el formato: 'Empresa | Posición'.
Tu objetivo es inferir el País (y Ciudad si es posible) más probable de esa persona.

REGLAS:
1. Si el texto menciona una ubicación explícitamente (ej. "Cancún", "CDMX", "Madrid", "Colombia"), extrae esa ciudad y el país correspondiente.
2. Ten cuidado con texto corrupto o en cirílico como "Kанкун, ROO" -> Esto es Cancún, México.
3. Si es una empresa que opera casi exclusivamente en un país específico (ej. "Mercado Libre", "Clip", "Konfío"), asume la sede principal.
4. Si no hay indicios geográficos, pon "Desconocido".
5. Los países deben estar en español.

RESPONDE ESTRICTAMENTE CON UN ARRAY JSON VÁLIDO. SIN TEXTO ANTES NI DESPUÉS.
Formato esperado:
[
  { "input": "Kанкун, ROO | Director", "country": "México", "city": "Cancún" },
  { "input": "Clip | Data Scientist", "country": "México", "city": "CDMX" }
]

Strings a analizar:
"""
    for s in batch:
        prompt += f"- {s}\n"
        
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            temperature=0.0,
            system="Responde estricta y únicamente con un Array JSON válido. No uses markdown.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        start_idx = content.find("[")
        end_idx = content.rfind("]")
        if start_idx != -1 and end_idx != -1:
            return json.loads(content[start_idx:end_idx+1])
        return []
    except Exception as e:
        print(f"Error en batch con Claude: {e}")
        return []

def main():
    print(f"Leyendo '{csv_path}'...")
    unique_strings = get_unique_strings()
    print(f"Encontrados {len(unique_strings)} strings únicos de 'Empresa | Posición'.")
    
    if not unique_strings:
        print("No hay datos para normalizar.")
        return
        
    batch_size = 30
    all_results = {}
    
    print("Enviando batches a Claude 3 Haiku...")
    for i in range(0, len(unique_strings), batch_size):
        batch = unique_strings[i:i+batch_size]
        print(f"  Procesando batch {i//batch_size + 1} de {(len(unique_strings) + batch_size - 1)//batch_size}...")
        
        results = normalize_batch(batch)
        for res in results:
            all_results[res.get("input", "")] = {
                "country": res.get("country", "Desconocido"),
                "city": res.get("city", "Desconocido")
            }
        time.sleep(1)
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
        
    print(f"\n[✓] ¡Éxito! El diccionario de normalización se ha guardado en '{output_path}'")
    print(f"    Total de ubicaciones normalizadas: {len(all_results)}")

if __name__ == "__main__":
    main()
