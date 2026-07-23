import re

input_file = "filtered_clip_congrats.txt"
output_file = "extracted_achievements.txt"

# Keywords that suggest a real human congratulating you on an achievement or talking about goals
achievement_keys = [
    r"crack", r"podio", r"podium", r"meta", r"cuota", r"rebas", r"attainment",
    r"overachieve", r"ganaste", r"premio", r"reconocimiento", r"logro", r"top",
    r"felicitaciones", r"felicidades"
]

rx = re.compile("|".join(achievement_keys), re.IGNORECASE)

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("================================================================================\n")

printed = 0
with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Scanning through {len(blocks)} blocks...\n\n")
    
    for idx, block in enumerate(blocks):
        block_lower = block.lower()
        
        is_automated_spam = (
            "aniversario de trabajo" in block_lower or 
            "nuevo puesto" in block_lower or 
            "new role" in block_lower or
            "talently" in block_lower or
            "salesforce" in block_lower or
            "docusign" in block_lower or
            "abriendo una beca" in block_lower or
            "it spark" in block_lower or
            "open english" in block_lower or
            "bonda" in block_lower or
            "multibank" in block_lower or
            "deel" in block_lower or
            "y combinator" in block_lower or
            "treble" in block_lower or
            "unirse a nuestro equipo" in block_lower
        )
        
        if rx.search(block_lower) and not is_automated_spam:
            out.write(f"--- MATCH {printed+1} ---\n")
            out.write(block.strip() + "\n")
            out.write("-" * 80 + "\n\n")
            printed += 1

print(f"Completed. Found {printed} non-spam achievement matches. Written to {output_file}")
