import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Rich_Media.csv"

with open("rich_media_details.txt", "w", encoding="utf-8") as out:
    with zipfile.ZipFile(zip_path, 'r') as z:
        if file_name not in z.namelist():
            out.write("Rich_Media.csv NOT found in ZIP.\n")
        else:
            with z.open(file_name) as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                header = next(reader)
                out.write("Header: " + " | ".join(header) + "\n\n")
                
                for idx, row in enumerate(reader, start=1):
                    out.write(f"Row {idx}: " + " | ".join(row) + "\n")

print("Done. Details written to rich_media_details.txt")
