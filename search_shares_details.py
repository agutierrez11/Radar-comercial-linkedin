import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Shares_577732310.csv"

patterns = [
    re.compile(r"performance", re.IGNORECASE),
    re.compile(r"performer", re.IGNORECASE),
    re.compile(r"podio", re.IGNORECASE),
    re.compile(r"podium", re.IGNORECASE),
    re.compile(r"reconocimiento", re.IGNORECASE),
    re.compile(r"logro", re.IGNORECASE),
    re.compile(r"felicit", re.IGNORECASE),
    re.compile(r"premi", re.IGNORECASE),
    re.compile(r"\btop\b", re.IGNORECASE)
]

with open("shares_matches_details.txt", "w", encoding="utf-8") as out:
    out.write("Searching Shares_577732310.csv details...\n\n")
    with zipfile.ZipFile(zip_path, 'r') as z:
        if file_name in z.namelist():
            with z.open(file_name) as f:
                stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                reader = csv.reader(stream)
                header = next(reader)
                
                matches = 0
                for idx, row in enumerate(reader, start=1):
                    row_str = " | ".join(row)
                    matched_patterns = [p.pattern for p in patterns if p.search(row_str)]
                    if matched_patterns:
                        out.write(f"Row {idx} - Matches: {matched_patterns}\n")
                        out.write(f"Date: {row[0]}\n")
                        out.write(f"Link: {row[1]}\n")
                        out.write(f"Text:\n{row[2]}\n")
                        out.write("=" * 80 + "\n\n")
                        matches += 1
                out.write(f"\nTotal matches in Shares: {matches}\n")

print("Completed. Results written to shares_matches_details.txt")
