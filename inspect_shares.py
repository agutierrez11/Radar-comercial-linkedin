import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Shares_577732310.csv"

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(file_name) as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        
        try:
            header = next(reader)
            print("Header:", header)
        except StopIteration:
            print("File is empty.")
            sys.exit(0)
            
        matches_found = 0
        for i, row in enumerate(reader, start=1):
            row_str = " | ".join(row)
            row_lower = row_str.lower()
            
            # Look for clip, performance, top, or felicit
            if "clip" in row_lower or "performance" in row_lower or "top" in row_lower or "felicit" in row_lower:
                print(f"Match found in row {i}:")
                # Print safe representation of row_str to prevent console crashes
                safe_str = row_str.encode('ascii', 'ignore').decode('ascii')
                print(f"  {safe_str[:300]}...")
                matches_found += 1

print(f"\nDone. Found {matches_found} matching rows in Shares.")
