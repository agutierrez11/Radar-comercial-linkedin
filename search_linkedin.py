import zipfile
import csv
import io
import re
import sys

# Ensure UTF-8 stdout just in case
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

zip_paths = [
    r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip",
    r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip (1).zip"
]

# Let's search broadly for clip, performance, performer, top, felicitacion, etc.
keywords = {
    "clip": re.compile(r"\bclip\b", re.IGNORECASE),
    "performance": re.compile(r"performance", re.IGNORECASE),
    "performer": re.compile(r"performer", re.IGNORECASE),
    "felicit": re.compile(r"felicit", re.IGNORECASE),
    "top": re.compile(r"\btop\b", re.IGNORECASE)
}

output_file = "search_results.md"

with open(output_file, "w", encoding="utf-8") as out:
    out.write("# LinkedIn Search Results\n\n")
    
    for zip_path in zip_paths:
        out.write(f"## ZIP File: `{zip_path}`\n\n")
        print(f"Searching in {zip_path}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                for file_name in z.namelist():
                    if not file_name.endswith('.csv'):
                        continue
                    
                    with z.open(file_name) as f:
                        text_stream = io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                        reader = csv.reader(text_stream)
                        
                        try:
                            header = next(reader)
                        except StopIteration:
                            continue
                        
                        for row_idx, row in enumerate(reader, start=1):
                            row_str = " | ".join(row)
                            row_lower = row_str.lower()
                            
                            # Define matches
                            matched_kws = [k for k, rx in keywords.items() if rx.search(row_str)]
                            
                            if not matched_kws:
                                continue
                            
                            # Let's check relevance criteria:
                            # 1. "clip" is mentioned AND (any of "top", "performance", "performer", "felicit")
                            # 2. Or "top performance" or "top performer" is mentioned
                            # 3. Or just "clip" is mentioned (let's show it so we don't miss anything)
                            is_relevant = False
                            if "clip" in row_lower:
                                is_relevant = True
                            elif "top performance" in row_lower or "top performer" in row_lower:
                                is_relevant = True
                            elif "felicit" in row_lower and "performance" in row_lower:
                                is_relevant = True
                            
                            if is_relevant:
                                out.write(f"### File: `{file_name}` | Row: {row_idx}\n")
                                out.write(f"**Matched Keywords:** {', '.join(matched_kws)}\n\n")
                                out.write("```text\n")
                                # Write clean text replacing formatting issues
                                out.write(row_str.strip() + "\n")
                                out.write("```\n\n")
                                out.write("---\n\n")
                                
        except Exception as e:
            out.write(f"**Error reading zip file:** {e}\n\n")
            print(f"Error: {e}")

print("Search completed. Results written to search_results.md")
