import subprocess, re, json

commits_raw = subprocess.check_output(['git', 'log', '--oneline', '-n', '30'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
commits = [line.split()[0] for line in commits_raw.strip().split('\n')]

print(f"Fast analyzing {len(commits)} commits...")

for c in commits:
    try:
        content = subprocess.check_output(['git', 'show', f'{c}:index.html'], cwd='c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial').decode('utf-8')
        # Check if 447 is written anywhere in index.html text, comments, or hardcoded values
        if '447' in content:
            matches = [m.start() for m in re.finditer('447', content)]
            print(f"🎯 MATCH IN COMMIT {c}: found '447' {len(matches)} times!")
            for pos in matches[:3]:
                snippet = content[max(0, pos-40):min(len(content), pos+40)]
                print(f"   Snippet: {snippet.replace(chr(10), ' ')}")
    except Exception as err:
        pass
