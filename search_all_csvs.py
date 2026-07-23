import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

keywords = [
    re.compile(r"performance", re.IGNORECASE),
    re.compile(r"performer", re.IGNORECASE),
    re.compile(r"podio", re.IGNORECASE),
    re.compile(r"podium", re.IGNORECASE),
    re.compile(r"attainment", re.IGNORECASE),
    re.compile(r"overachieve", re.IGNORECASE)
]

with open("all_csv_matches.txt", "w", encoding="utf-8") as out:
    out.write("Searching ALL CSVs inside the ZIP...\n\n")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in z.namelist():
            if not file_name.endswith('.csv'):
                continue
            
            try:
                with z.open(file_name) as f:
                    stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                    reader = csv.reader(stream)
                    try:
                        header = next(reader)
                    except StopIteration:
                        continue
                    
                    for idx, row in enumerate(reader, start=1):
                        row_str = " | ".join(row)
                        matched = [kw.pattern for kw in keywords if kw.search(row_str)]
                        if matched:
                            out.write(f"[{file_name}] Row {idx} - Matches: {matched}\n")
                            out.write(f"  Content: {row_str.strip()}\n")
                            out.write("-" * 80 + "\n\n")
            except Exception as e:
                out.write(f"Error reading {file_name}: {e}\n\n")

print("Completed. Results written to all_csv_matches.txt")
