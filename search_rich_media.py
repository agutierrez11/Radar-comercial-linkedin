import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Rich_Media.csv"

print("Searching Rich Media...")
with zipfile.ZipFile(zip_path, 'r') as z:
    if file_name in z.namelist():
        with z.open(file_name) as f:
            stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
            reader = csv.reader(stream)
            header = next(reader)
            print("Header:", header)
            for idx, row in enumerate(reader, start=1):
                row_str = " | ".join(row)
                row_lower = row_str.lower()
                if "clip" in row_lower or "performance" in row_lower or "top" in row_lower or "podio" in row_lower:
                    print(f"Row {idx}:")
                    print(row_str)
                    print("-" * 50)
