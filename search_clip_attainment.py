import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "messages.csv"

# Regex for numbers/percentages or achievement terms
achievement_keys = [
    r"\d{3}%", r"meta", r"cuota", r"cumpli", r"rebas", r"attainment", r"overachieve",
    r"podio", r"podium", r"primer", r"1er", r"n[oº]\.?\s*1", r"top", r"ranking", r"rank"
]
rx_achieve = re.compile("|".join(achievement_keys), re.IGNORECASE)

matches = []

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(file_name) as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        header = next(reader)
        
        for idx, row in enumerate(reader, start=1):
            date_str = row[6]
            content = row[8]
            sender = row[2]
            
            # Check date range (July 2021 - March 2025)
            date_match = re.search(r"(\d{4})-\d{2}-\d{2}", date_str)
            if date_match:
                year = int(date_match.group(1))
                if 2021 <= year <= 2025:
                    # Filter for years at Clip, more specifically:
                    is_clip = False
                    month_match = re.search(r"\d{4}-(\d{2})-\d{2}", date_str)
                    if month_match:
                        month = int(month_match.group(1))
                        if year == 2021 and month >= 7:
                            is_clip = True
                        elif 2022 <= year <= 2024:
                            is_clip = True
                        elif year == 2025 and month <= 3:
                            is_clip = True
                            
                    if is_clip and rx_achieve.search(content):
                        # Save
                        matches.append({
                            "row": idx,
                            "from": sender,
                            "to": row[4],
                            "date": date_str,
                            "content": content
                        })

# Write findings to a UTF-8 file
output_file = "clip_attainment_messages.txt"
with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} messages from Clip period discussing goals/achievements:\n\n")
    for m in matches:
        out.write(f"Row {m['row']} | From: {m['from']} | To: {m['to']} | Date: {m['date']}\n")
        out.write(f"Content: {m['content'].strip()}\n")
        out.write("-" * 80 + "\n\n")

print(f"Done. Found {len(matches)} messages. Written to {output_file}")
