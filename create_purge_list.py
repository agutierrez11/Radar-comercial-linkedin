import os
import re
import csv

# Paths
structured_vault = r"C:\Users\Antonio\Bovedas_Obsidian\Boveda_Estructurada"
folders_to_purge = {
    "03_Ghosts_Otros": "Ghosts - Sin Interacción",
    "04_Ruido": "Ruido / Basura"
}

output_csv = r"C:\Users\Antonio\OneDrive\Escritorio\Lista_de_Purga_LinkedIn.csv"
output_xlsx = r"C:\Users\Antonio\OneDrive\Escritorio\Lista_de_Purga_LinkedIn.xlsx"

purge_list = []

# Regex patterns
cargo_pat = re.compile(r"-\s*\*\*Cargo:\*\*\s*(?:\[\[)?([^\]\n]+)(?:\]\])?")
empresa_pat = re.compile(r"-\s*\*\*Empresa:\*\*\s*(?:\[\[)?([^\]\n]+)(?:\]\])?")
pais_pat = re.compile(r"-\s*\*\*País:\*\*\s*(?:\[\[)?([^\]\n]+)(?:\]\])?")
sector_pat = re.compile(r"-\s*\*\*Sector:\*\*\s*(?:\[\[)?([^\]\n]+)(?:\]\])?")
jerarquia_pat = re.compile(r"-\s*\*\*Jerarquía:\*\*\s*(?:\[\[)?([^\]\n]+)(?:\]\])?")
fecha_pat = re.compile(r"-\s*\*\*Fecha de Conexión:\*\*\s*(.*)")
linkedin_pat = re.compile(r"\((https://www.linkedin.com/in/[^\)]+)\)")

print("Scanning files for purge list...")

for folder, category in folders_to_purge.items():
    folder_path = os.path.join(structured_vault, folder)
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                filepath = os.path.join(folder_path, filename)
                name = filename[:-3]
                
                cargo = ""
                empresa = ""
                pais = ""
                sector = ""
                jerarquia = ""
                fecha = ""
                linkedin = ""
                
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        
                        m = cargo_pat.search(content)
                        if m: cargo = m.group(1).strip()
                        
                        m = empresa_pat.search(content)
                        if m: empresa = m.group(1).strip()
                        
                        m = pais_pat.search(content)
                        if m: pais = m.group(1).strip()
                        
                        m = sector_pat.search(content)
                        if m: sector = m.group(1).strip()
                        
                        m = jerarquia_pat.search(content)
                        if m: jerarquia = m.group(1).strip()
                        
                        m = fecha_pat.search(content)
                        if m: fecha = m.group(1).strip()
                        
                        m = linkedin_pat.search(content)
                        if m: linkedin = m.group(1).strip()
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                
                purge_list.append({
                    "Nombre": name,
                    "Cargo": cargo,
                    "Empresa": empresa,
                    "País": pais,
                    "Sector": sector,
                    "Jerarquía": jerarquia,
                    "Fecha de Conexión": fecha,
                    "LinkedIn URL": linkedin,
                    "Clasificación": category
                })

print(f"Compiled {len(purge_list)} contacts to purge.")

# 1. Try to write XLSX using pandas/openpyxl
xlsx_written = False
try:
    import pandas as pd
    df = pd.DataFrame(purge_list)
    # Sort by Classification and Name
    df.sort_values(by=["Clasificación", "Nombre"], inplace=True)
    df.to_excel(output_xlsx, index=False)
    print(f"Successfully created Excel file at: {output_xlsx}")
    xlsx_written = True
except ImportError:
    print("pandas/openpyxl not installed. Falling back to CSV.")
except Exception as e:
    print(f"Error creating Excel: {e}. Falling back to CSV.")

# 2. Write CSV (Excel-compatible with UTF-8 BOM)
try:
    with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Nombre", "Cargo", "Empresa", "País", "Sector", "Jerarquía", "Fecha de Conexión", "LinkedIn URL", "Clasificación"
        ], delimiter=";") # Semi-colon delimiter is preferred by Excel in Spanish locales
        writer.writeheader()
        # Sort purge list by Classification and Name
        sorted_list = sorted(purge_list, key=lambda x: (x["Clasificación"], x["Nombre"]))
        writer.writerows(sorted_list)
    print(f"Successfully created CSV file at: {output_csv}")
except Exception as e:
    print(f"Error creating CSV: {e}")

print("Done!")
