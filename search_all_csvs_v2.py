import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

keywords = [
    re.compile(r"reconocimiento", re.IGNORECASE),
    re.compile(r"premio", re.IGNORECASE),
    re.compile(r"destacado", re.IGNORECASE),
    re.compile(r"logro", re.IGNORECASE),
    re.compile(r"ganador", re.IGNORECASE),
    re.compile(r"campe[oó]n", re.IGNORECASE),
    re.compile(r"bono", re.IGNORECASE),
    re.compile(r"rank", re.IGNORECASE),
    re.compile(r"felicidades", re.IGNORECASE),
    re.compile(r"felicitaciones", re.IGNORECASE),
    re.compile(r"podio", re.IGNORECASE),
    re.compile(r"podium", re.IGNORECASE)
]

with open("all_csv_matches_v2.txt", "w", encoding="utf-8") as out:
    out.write("Searching ALL CSVs inside the ZIP for Expanded Keywords...\n\n")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in z.namelist():
            if not file_name.endswith('.csv'):
                continue
            
            # Skip messages.csv in this broad write if it's too huge, or search it selectively.
            # messages.csv is about 9MB. We can search it but only output if it's during the Clip era (July 2021 - March 2025).
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
                        
                        # Apply date filters to big files if possible
                        if file_name == "messages.csv":
                            # Date is at index 6 in messages.csv
                            date_str = row[6]
                            date_match = re.search(r"(\d{4})-\d{2}-\d{2}", date_str)
                            if date_match:
                                year = int(date_match.group(1))
                                if not (2021 <= year <= 2025):
                                    continue
                        
                        matched = [kw.pattern for kw in keywords if kw.search(row_str)]
                        if matched:
                            # Skip automatic anniversary template messages to reduce noise
                            if "cumplir" in row_str.lower() and "año" in row_str.lower() and "clip" in row_str.lower() and "felicidades" in row_str.lower():
                                continue
                            
                            # Skip standard job post outreach if it is spammy
                            if "open english" in row_str.lower() or "deel" in row_str.lower():
                                continue
                                
                            out.write(f"[{file_name}] Row {idx} - Matches: {matched}\n")
                            out.write(f"  Content: {row_str.strip()[:600]}\n")
                            out.write("-" * 80 + "\n\n")
            except Exception as e:
                out.write(f"Error reading {file_name}: {e}\n\n")

print("Completed. Results written to all_csv_matches_v2.txt")
