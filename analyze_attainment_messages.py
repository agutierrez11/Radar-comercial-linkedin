import re

input_file = "clip_attainment_messages.txt"
output_file = "clip_internal_attainment.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("-" * 80 + "\n\n")

print(f"Total blocks to analyze: {len(blocks)}")
filtered = []

# Keywords indicating self-promotion pitch to prospects (which we want to exclude)
pitch_indicators = [
    r"llevo algunos meses dando vueltas", r"me pongo en contacto contigo",
    r"si te interesa integrar", r"opción de pago", r"pasarela de pago",
    r"soluciones de cobro contra entrega", r"cobros a distancia", r"puntos que mencionas",
    r"ofrecerles el servicio de", r"si te interesa conocer más", r"quisiera platicarte"
]
pitch_rx = re.compile("|".join(pitch_indicators), re.IGNORECASE)

# Keywords indicating personal or performance discussion
personal_indicators = [
    r"crack", r"podio", r"podium", r"attainment", r"performance", r"performer",
    r"felicidad", r"felicit", r"meta", r"cuota", r"cumpli", r"rebas", r"logro",
    r"tabla", r"número\s*1", r"n[oº]\.?\s*1", r"top"
]
personal_rx = re.compile("|".join(personal_indicators), re.IGNORECASE)

for block in blocks:
    block_lower = block.lower()
    
    # Let's filter out standard pitches
    if pitch_rx.search(block_lower):
        continue
        
    # We want to check if it's a conversation with colleagues or discussing personal performance
    # For example, containing "performance", "attainment", "performer", "crack", etc.
    # or discussing details of quota/goals
    if personal_rx.search(block_lower):
        # Filter out sponsored ads or recruiting spam (like Open English, Deel, Bonda, etc.)
        is_spam = (
            "open english" in block_lower or 
            "deel" in block_lower or 
            "bonda" in block_lower or 
            "multibank" in block_lower or
            "talently" in block_lower or
            "salesforce" in block_lower or
            "docusign" in block_lower
        )
        if not is_spam:
            filtered.append(block)

# Sort them (they are already chronologically ordered if we keep them in order of messages.csv)
with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(filtered)} filtered internal or performance conversations during Clip period:\n\n")
    for block in filtered:
        out.write(block)
        out.write("=" * 80 + "\n\n")

print(f"Completed. Filtered down to {len(filtered)} messages. Written to {output_file}")
