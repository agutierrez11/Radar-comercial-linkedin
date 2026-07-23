import csv
import json
import zipfile
import os

with open('locations_normalized.json', 'r', encoding='utf-8') as f:
    loc_data = json.load(f)

# Leer audited_connections y escribir Cleaned_Connections.csv
in_csv = 'audited_connections.csv'
out_csv = 'Connections.csv' # Le ponemos el nombre original para que el dashboard lo lea bien

with open(in_csv, 'r', encoding='utf-8-sig') as f_in, open(out_csv, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames + ['Country_AI', 'City_AI']
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        company = row.get("Company", "").strip()
        position = row.get("Position", "").strip()
        key = f"{company} | {position}"
        
        if key in loc_data:
            row['Country_AI'] = loc_data[key].get('country', '')
            row['City_AI'] = loc_data[key].get('city', '')
        else:
            row['Country_AI'] = 'Desconocido'
            row['City_AI'] = 'Desconocido'
            
        writer.writerow(row)

# Empacar en ZIP
zip_filename = 'LinkedinData_Cleaned.zip'
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(out_csv, arcname='Connections.csv')
    
print(f"Creado {zip_filename} con los datos limpios.")
