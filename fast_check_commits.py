import subprocess, re

commits = ['952fed9', '0018d4d', '19c8326', 'eed7fec', '26f8973', '774b30e', '00e1791', 'c089e92', '033c674']

for c in commits:
    try:
        content = subprocess.check_output(['git', 'show', f'{c}:index.html'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
        # Find purge candidate logic or criteria definitions
        criteria_match = re.search(r'criteria:\s*\[(.*?)\]\s*,', content, re.DOTALL)
        if criteria_match:
            print(f"=== Commit {c} Criteria ===")
            crit_text = criteria_match.group(1)
            # Find all labels and on states
            items = re.findall(r"label:\s*'([^']+)'.*?on:\s*(true|false)", crit_text, re.DOTALL)
            for label, state in items:
                print(f"  - {label}: {state}")
    except Exception as err:
        print(f"Error checking commit {c}: {err}")
