import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Positions.csv"

with open("positions_details.txt", "w", encoding="utf-8") as out:
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(file_name) as f:
            stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
            reader = csv.reader(stream)
            header = next(reader)
            
            out.write("Positions Header: " + " | ".join(header) + "\n\n")
            for idx, row in enumerate(reader, start=1):
                out.write(f"Row {idx}:\n")
                out.write(f"  Company Name: {row[0]}\n")
                out.write(f"  Title: {row[1]}\n")
                out.write(f"  Location: {row[2]}\n")
                out.write(f"  Start Date: {row[3]}\n")
                out.write(f"  End Date: {row[4]}\n")
                out.write(f"  Description: {row[5]}\n")
                out.write("-" * 80 + "\n\n")

print("Done. Details written to positions_details.txt")
