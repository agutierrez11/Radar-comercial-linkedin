import subprocess, re, json

# Let's inspect index.html at commits around 12pm-4pm today: 952fed9, 0018d4d, 19c8326, 26f8973, 00e1791, c089e92
commits = ['952fed9', '0018d4d', '19c8326', '26f8973', '00e1791', 'c089e92', '033c674']

for c in commits:
    try:
        content = subprocess.check_output(['git', 'show', f'{c}:index.html'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
        
        # Check default criteria states
        criteria = re.findall(r"id:\s*'([^']+)'.*?label:\s*'([^']+)'.*?on:\s*(true|false)", content, re.DOTALL)
        
        # Check master contacts length or inline dataset if hardcoded
        contacts_len = len(re.findall(r'\{[^{}]*name\s*:', content))
        
        print(f"Commit {c}:")
        print(f"  Criteria: {criteria}")
        print(f"  Contacts count in file snippet: {contacts_len}")
    except Exception as e:
        print(f"Error {c}: {e}")
