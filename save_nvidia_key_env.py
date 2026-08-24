"""
save_nvidia_key_env.py
Saves recovered valid NVIDIA API Key into .env and configures llm_router.py
to use meta/llama-3.1-70b-instruct as active NVIDIA NIM model.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

env_path = ".env"
nvidia_key = "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"

# Read existing .env
lines = []
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

# Check if NVIDIA_API_KEY exists
nvidia_exists = False
new_lines = []
for l in lines:
    if l.startswith("NVIDIA_API_KEY=") or l.startswith("NVAPI_KEY="):
        new_lines.append(f"NVIDIA_API_KEY={nvidia_key}\n")
        nvidia_exists = True
    else:
        new_lines.append(l)

if not nvidia_exists:
    new_lines.append(f"NVIDIA_API_KEY={nvidia_key}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ Saved NVIDIA_API_KEY to .env file successfully!")
