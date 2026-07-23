import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "Shares_577732310.csv"

# Keywords related to Clip or Orange
clip_keywords = re.compile(r"clip|orange|naranja|payclip", re.IGNORECASE)

matches = []

with zipfile.ZipFile(zip_path, 'r') as z:
    if file_name in z.namelist():
        with z.open(file_name) as f:
            stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
            reader = csv.reader(stream)
            header = next(reader)
            
            for idx, row in enumerate(reader, start=1):
                row_str = " | ".join(row)
                if clip_keywords.search(row_str):
                    matches.append({
                        "row": idx,
                        "date": row[0],
                        "link": row[1],
                        "text": row[2]
                    })

# Sort by date
matches.sort(key=lambda x: x["date"])

output_file = "clip_posts.txt"
with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} posts containing Clip, Orange, Naranja, or Payclip:\n\n")
    for m in matches:
        out.write(f"Row {m['row']} | Date: {m['date']}\n")
        out.write(f"Link: {m['link']}\n")
        out.write(f"Text:\n{m['text'].strip()}\n")
        out.write("=" * 80 + "\n\n")

print(f"Completed. Found {len(matches)} Clip-related posts. Written to {output_file}")
