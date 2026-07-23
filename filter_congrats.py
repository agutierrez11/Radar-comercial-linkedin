import re

input_file = "received_congrats.txt"
output_file = "filtered_clip_congrats.txt"

# Date range: July 2021 to March 2025
# e.g. "Date: 2023-04-25 17:37:01 UTC"
date_pattern = re.compile(r"Date:\s*(\d{4}-\d{2}-\d{2})")

blocks = []
current_block = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("Row "):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        elif current_block:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

filtered_blocks = []

for block in blocks:
    block_text = "".join(block)
    # Check date
    date_match = date_pattern.search(block_text)
    if date_match:
        date_str = date_match.group(1)
        year = int(date_str[:4])
        month = int(date_str[5:7])
        
        # Check if between July 2021 and March 2025
        is_in_clip_period = False
        if year == 2021 and month >= 7:
            is_in_clip_period = True
        elif 2022 <= year <= 2024:
            is_in_clip_period = True
        elif year == 2025 and month <= 3:
            is_in_clip_period = True
            
        if is_in_clip_period:
            # Let's filter out noise: some automated LinkedIn messages like "Felicidades por tu nuevo puesto"
            # are common, but let's keep them and mark them, and focus on personalized messages.
            # We want to search for keys like: crack, meta, podio, top, performance, performer, premio, logro, etc.
            block_lower = block_text.lower()
            
            # Words indicating performance/achievements rather than generic anniversary wishes:
            achievement_indicators = [
                "crack", "podio", "podium", "performance", "performer", "premio", 
                "logro", "meta", "cuota", "attainment", "overachieve", "campe", "ganad",
                "número 1", "top", "rebas", "ventas", "tabla", "cumpli", "destacado"
            ]
            
            # Check if it has any achievement indicators
            has_achievement = any(indicator in block_lower for indicator in achievement_indicators)
            
            # Also keep explicit congratulations that might have personal text
            is_generic_anniversary = "aniversario de trabajo" in block_lower or "nuevo puesto" in block_lower
            
            if has_achievement or not is_generic_anniversary:
                filtered_blocks.append((date_str, block_text))

# Sort by date
filtered_blocks.sort(key=lambda x: x[0])

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Filtered {len(filtered_blocks)} messages from the Clip period (Jul 2021 - Mar 2025):\n\n")
    for date, text in filtered_blocks:
        out.write(text)
        out.write("=" * 80 + "\n\n")

print(f"Filtered results written to {output_file}. Found {len(filtered_blocks)} matches.")
