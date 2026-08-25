import shutil
import os

art_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\brain\09b49656-7810-4a5e-933d-07a1cc545f79"
files = [
    "qa_test1_fresh_login_gating.png",
    "qa_test2_giovanna_isolated_vault.png",
    "qa_test3_antonio_master_admin.png"
]

for f in files:
    src = os.path.join(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial", f)
    dst = os.path.join(art_dir, f)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {f} to artifacts directory.")
