import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
files = ["Certifications.csv", "Endorsement_Received_Info.csv", "Recommendations_Given.csv"]

with open("extra_csv_details.txt", "w", encoding="utf-8") as out:
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in files:
            if file_name not in z.namelist():
                out.write(f"File {file_name} NOT found in ZIP.\n\n")
                continue
                
            out.write(f"=== File: {file_name} ===\n")
            with z.open(file_name) as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                try:
                    header = next(reader)
                    out.write("Header: " + " | ".join(header) + "\n\n")
                except StopIteration:
                    out.write("Empty file\n\n")
                    continue
                
                for idx, row in enumerate(reader, start=1):
                    out.write(f"Row {idx}: " + " | ".join(row) + "\n")
            out.write("-" * 80 + "\n\n")

print("Done. Details written to extra_csv_details.txt")
