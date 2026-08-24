import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

brain_path = r"C:\Users\Antonio\.gemini\antigravity-ide\brain"
transcripts = glob.glob(os.path.join(brain_path, "*", ".system_generated", "logs", "transcript*.jsonl"))

print(f"Buscando en {len(transcripts)} transcripciones de conversaciones anteriores...")

found_keys = set()
for t_file in transcripts:
    try:
        with open(t_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if 'nvapi-' in line:
                    idx = 0
                    while True:
                        idx = line.find('nvapi-', idx)
                        if idx == -1:
                            break
                        chunk = line[idx:idx+70]
                        # Extract clean key
                        clean_key = chunk.split('\\')[0].split('"')[0].split("'")[0].split()[0].strip()
                        if len(clean_key) >= 20:
                            found_keys.add((t_file, clean_key))
                        idx += 6
    except Exception:
        pass

print(f"\n==========================================")
print(f"CLAVES ENCONTRADAS: {len(found_keys)}")
print("==========================================")
for path, key in found_keys:
    print(f"Conversation Log: {os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(path))))}")
    print(f"Clave Completa: {key}")
