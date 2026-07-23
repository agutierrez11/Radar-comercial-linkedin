import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "messages.csv"

patterns = [
    re.compile(r"felicit", re.IGNORECASE),
    re.compile(r"felicida", re.IGNORECASE),
    re.compile(r"congrat", re.IGNORECASE),
    re.compile(r"top performance", re.IGNORECASE),
    re.compile(r"top performer", re.IGNORECASE),
    re.compile(r"podio", re.IGNORECASE),
    re.compile(r"podium", re.IGNORECASE),
    re.compile(r"reconocimiento", re.IGNORECASE)
]

with open("messages_results.txt", "w", encoding="utf-8") as out:
    out.write("Searching messages.csv...\n\n")
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(file_name) as f:
            stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
            reader = csv.reader(stream)
            header = next(reader)
            
            for i, row in enumerate(reader, start=1):
                row_str = " | ".join(row)
                matched = [p.pattern for p in patterns if p.search(row_str)]
                if matched:
                    out.write(f"Row {i} - Matches: {matched}\n")
                    out.write(f"  From: {row[2]} | To: {row[4]} | Date: {row[6]}\n")
                    out.write(f"  Content: {row_str.strip()}\n")
                    out.write("-" * 80 + "\n\n")

print("Completed. Results written to messages_results.txt")
