import re

input_file = "all_csv_matches_v2.txt"
output_file = "achievements_v2_summary.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("--------------------------------------------------------------------------------\n\n")

print(f"Total blocks in all_csv_matches_v2: {len(blocks)}")
matches = []

for block in blocks:
    block_lower = block.lower()
    
    # We want to filter for messages received/sent during Clip era (2021 - 2025)
    # Check if this is messages.csv and look for Clip-era dates
    # We also want to look for actual congratulations or awards
    
    # Check if the block mentions the Clip era date (from messages.csv or other CSVs)
    # e.g., 2021, 2022, 2023, 2024, 2025
    date_match = re.search(r"202[1-5]-\d{2}-\d{2}", block)
    if date_match:
        # Check if the message is congratulating Antonio or discussing his achievements.
        # Let's filter out messages sent BY Antonio where he says "muchas felicidades por el nuevo reto" 
        # or "felicidades por tu aniversario", because those are him congratulating others.
        # We want to keep messages from OTHERS to Antonio, OR messages sent by Antonio where he discusses his achievements.
        
        # If it is a message from Antonio congratulating someone else:
        if "from: 💳antonio gutiérrez" in block_lower:
            # Check if he is talking about himself
            # e.g., "yo", "mi meta", "cumplí", "quedé", "fui"
            personal_keywords = [r"\byo\b", r"\bmi\b", r"cumpl[í|é]", r"gan[é|ar]", r"logr[é|ar]", r"qued[é|ar]", r"fui", r"attainment", r"cuota"]
            if not any(re.search(pk, block_lower) for pk in personal_keywords):
                continue
                
        # If it's an anniversary greeting:
        if "aniversario de trabajo" in block_lower or "cumplir 3 años en clip" in block_lower or "cumplir 3 años" in block_lower:
            continue
            
        # If it's recruiter outreach or system templates:
        if "didi - te estamos buscando" in block_lower or "tencent meeting" in block_lower or "sorteo" in block_lower:
            continue
            
        matches.append(block.strip())

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} relevant performance/congratulatory matches in V2:\n\n")
    for idx, m in enumerate(matches, start=1):
        out.write(f"--- MATCH {idx} ---\n")
        out.write(m + "\n")
        out.write("-" * 80 + "\n\n")

print(f"Refined V2 matches written to {output_file}. Found {len(matches)} results.")
