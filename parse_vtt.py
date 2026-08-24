import re

def clean_vtt(vtt_file, output_file):
    with open(vtt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    unique_lines = []
    last_line = ""
    for line in lines:
        line = line.strip()
        # Skip header, timestamps, empty lines
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:') or '-->' in line:
            continue
        # Remove tags like <00:00:00.000><c>
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean and clean != last_line:
            unique_lines.append(clean)
            last_line = clean

    full_text = " ".join(unique_lines)
    # Deduplicate consecutive words or short phrases caused by VTT auto-sub scrolling
    words = full_text.split()
    dedup_words = []
    for w in words:
        if not dedup_words or w != dedup_words[-1]:
            dedup_words.append(w)

    final_text = " ".join(dedup_words)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)
    
    print(f"Cleaned {vtt_file} -> {output_file}: {len(final_text)} chars, {len(dedup_words)} words")
    return final_text

t1 = clean_vtt('v1_sub.es.vtt', 'video1_clean.txt')
t2 = clean_vtt('v2_sub.es.vtt', 'video2_clean.txt')
