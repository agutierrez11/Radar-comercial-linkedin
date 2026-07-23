import re

input_file = "all_csv_matches_v2.txt"
output_file = "achievements_v3_summary.txt"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

blocks = content.split("--------------------------------------------------------------------------------\n\n")

print(f"Total blocks in all_csv_matches_v2: {len(blocks)}")
matches = []

# Personal words for outgoing messages
personal_indicators = [
    r"cumpl[íé]", r"gan[éó]", r"logr[éó]", r"qued[éó]", r"fui", r"attainment", r"cuota", r"meta",
    r"podio", r"podium", r"mi\s+número", r"mi\s+performance", r"mi\s+meta", r"mi\s+resultado",
    r"mis\s+números", r"mis\s+resultados", r"mis\s+metas"
]
personal_rx = re.compile("|".join(personal_indicators), re.IGNORECASE)

# Keywords for incoming messages
incoming_indicators = [
    r"felicidad", r"felicit", r"crack", r"podio", r"podium", r"performer", r"performance",
    r"attainment", r"overachieve", r"meta", r"cuota", r"rebas", r"logro", r"lugar", r"ranking", r"tabla"
]
incoming_rx = re.compile("|".join(incoming_indicators), re.IGNORECASE)

for block in blocks:
    if not block.strip():
        continue
        
    # Find the Content line
    content_match = re.search(r"Content:\s*(.*)", block)
    if not content_match:
        continue
        
    row_content = content_match.group(1)
    fields = row_content.split(" | ")
    
    if len(fields) < 9:
        continue
        
    sender_name = fields[2].strip()
    recipient_name = fields[4].strip()
    date_str = fields[6].strip()
    message_text = fields[8].strip()
    
    message_lower = message_text.lower()
    
    # Filter by Clip era (July 2021 - March 2025)
    date_match = re.search(r"(\d{4})-\d{2}-\d{2}", date_str)
    if not date_match:
        continue
    year = int(date_match.group(1))
    if not (2021 <= year <= 2025):
        continue
        
    month_match = re.search(r"\d{4}-(\d{2})-\d{2}", date_str)
    if month_match:
        month = int(month_match.group(1))
        if year == 2021 and month < 7:
            continue
        if year == 2025 and month > 3:
            continue
            
    # Exclude anniversary templates or generic congrats
    if "cumplir" in message_lower and "año" in message_lower and "clip" in message_lower:
        continue
    if "aniversario de trabajo" in message_lower:
        continue
    if "didi - te estamos buscando" in message_lower or "tencent meeting" in message_lower or "sorteo" in message_lower:
        continue
        
    is_from_antonio = "antonio" in sender_name.lower() or "gtzj" in sender_name.lower()
    
    if is_from_antonio:
        # Outgoing message - did Antonio talk about his own performance/goals?
        if personal_rx.search(message_lower):
            matches.append({
                "block": block,
                "type": "OUTGOING (Antonio -> Others)",
                "sender": sender_name,
                "recipient": recipient_name,
                "date": date_str,
                "message": message_text
            })
    else:
        # Incoming message - did someone else congratulate or discuss performance with Antonio?
        if incoming_rx.search(message_lower):
            matches.append({
                "block": block,
                "type": "INCOMING (Others -> Antonio)",
                "sender": sender_name,
                "recipient": recipient_name,
                "date": date_str,
                "message": message_text
            })

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} highly relevant Clip-era performance messages:\n\n")
    for idx, m in enumerate(matches, start=1):
        out.write(f"--- MATCH {idx} ({m['type']}) ---\n")
        out.write(f"Date: {m['date']}\n")
        out.write(f"From: {m['sender']} | To: {m['recipient']}\n")
        out.write(f"Message: {m['message']}\n")
        out.write("-" * 80 + "\n\n")

print(f"Refined V3 matches written to {output_file}. Found {len(matches)} results.")
