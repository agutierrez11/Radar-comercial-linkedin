import zipfile
import csv
import io

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
files = ["Positions.csv", "Profile.csv", "Profile Summary.csv"]

with open("profile_results.txt", "w", encoding="utf-8") as out:
    out.write("Searching Profile/Position files...\n\n")
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in files:
            if file_name in z.namelist():
                out.write(f"\n=== {file_name} ===\n")
                with z.open(file_name) as f:
                    stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                    reader = csv.reader(stream)
                    header = next(reader)
                    out.write(f"Header: {header}\n")
                    for idx, row in enumerate(reader, start=1):
                        row_str = " | ".join(row)
                        out.write(f"Row {idx}:\n{row_str}\n")
                        out.write("-" * 80 + "\n")

print("Completed. Results written to profile_results.txt")
