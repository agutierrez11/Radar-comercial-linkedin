import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Shares_577732310.csv"

print("--- FULL POST FROM ROW 282 ---")
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(file_name) as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        header = next(reader)
        
        for i, row in enumerate(reader, start=1):
            if i == 282:
                for col_name, val in zip(header, row):
                    print(f"{col_name}:")
                    print(val)
                    print("="*40)
                break
