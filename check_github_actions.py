import urllib.request
import json

url = "https://api.github.com/repos/agutierrez11/Radar-comercial-linkedin/actions/runs"
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        runs = data.get('workflow_runs', [])
        print(f"Encontrados {len(runs)} ejecuciones de workflows.")
        for r in runs[:5]:
            print(f"ID: {r['id']} | Evento: {r['event']} | Rama: {r['head_branch']} | Commit: {r['head_commit']['message'][:40]} | Estado: {r['status']} | Conclusión: {r['conclusion']}")
except Exception as e:
    print(f"Error al conectar con la API de GitHub: {e}")
