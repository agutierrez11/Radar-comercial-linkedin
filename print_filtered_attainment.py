import re

input_file = "clip_internal_attainment.txt"
output_file = "achievements_summary.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("================================================================================\n")

print(f"Total blocks in clip_internal_attainment: {len(blocks)}")
matches = []

# Keywords to look for in the filtered messages
keywords = [
    r"top\s*performer", r"top\s*performance", r"attainment", r"overachieve", 
    r"rebas", r"podio", r"podium", r"meta", r"cuota", r"cumpli", r"crack", r"lugar",
    r"tabla", r"número\s*1", r"rank"
]
rx = re.compile("|".join(keywords), re.IGNORECASE)

for block in blocks:
    block_lower = block.lower()
    
    # We want to check if the message is actually about Antonio's own results, goals, or ranking.
    # We can exclude general chit-chat and focus on content mentioning actual sales figures or performance terms.
    if rx.search(block_lower):
        # Let's filter out some common noise (e.g. general references to ChatGPT / DAN, or other people's job postings)
        if "chatgpt successfully jailbroken" in block_lower or "tencent meeting" in block_lower:
            continue
        matches.append(block.strip())

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} relevant performance matches:\n\n")
    for idx, m in enumerate(matches, start=1):
        out.write(f"--- MATCH {idx} ---\n")
        out.write(m + "\n")
        out.write("-" * 80 + "\n\n")

print(f"Refined matches written to {output_file}. Found {len(matches)} results.")
