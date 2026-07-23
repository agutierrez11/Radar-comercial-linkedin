import zipfile
import csv
import io
import re

zip_path = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"
file_name = "messages.csv"

# Achievement keywords
keywords = [
    r"felicit", r"felicida", r"congrat", r"crack", r"podio", r"podium", 
    r"performance", r"performer", r"premio", r"logro", r"reconocimiento",
    r"cuota", r"meta", r"attainment", r"overachieve", r"campe", r"ganad",
    r"número\s*1", r"n[oº]\.?\s*1", r"top"
]

rx = re.compile("|".join(keywords), re.IGNORECASE)

print("Searching for achievements in received messages...")
matches = []

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open(file_name) as f:
        stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
        reader = csv.reader(stream)
        header = next(reader)
        
        for idx, row in enumerate(reader, start=1):
            sender = row[2]
            content = row[8]
            date = row[6]
            
            # Exclude messages sent by Antonio
            if "antonio" in sender.lower():
                continue
                
            if rx.search(content):
                # Save details
                matches.append({
                    "row": idx,
                    "from": sender,
                    "date": date,
                    "content": content
                })

# Write findings to a UTF-8 file
output_file = "received_congrats.txt"
with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} received messages with achievement keywords:\n\n")
    for m in matches:
        out.write(f"Row {m['row']} | From: {m['from']} | Date: {m['date']}\n")
        out.write(f"Content: {m['content'].strip()}\n")
        out.write("-" * 80 + "\n\n")

print(f"Done. Found {len(matches)} potential messages. Written to {output_file}")
