import shutil
import os

art_dir = r"C:\Users\Antonio\.gemini\antigravity-ide\brain\09b49656-7810-4a5e-933d-07a1cc545f79"
files = [
    "qa_test4_monthly_reminder_banner.png",
    "qa_test5_monthly_reminder_modal.png",
    "qa_test6_monthly_reminder_dismissed.png"
]

for f in files:
    src = os.path.join(r"c:\Users\Antonio\.gemini\antigravity-ide\scratch\radar-comercial", f)
    dst = os.path.join(art_dir, f)
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"Copied {f} to artifacts directory.")
