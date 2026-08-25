import urllib.request
import json

url = "https://api.github.com/repos/agutierrez11/Radar-comercial-linkedin/actions/runs?per_page=10"
req = urllib.request.Request(url, headers={"User-Agent": "Python", "Accept": "application/vnd.github+json"})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        for run in data.get("workflow_runs", []):
            print(f"Run ID: {run['id']} | Name: {run['name']} | Status: {run['status']} | Conclusion: {run['conclusion']} | HTML URL: {run['html_url']}")
except Exception as e:
    print("Error fetching GitHub Actions runs:", e)
