import requests
import json

API_KEY = "6KIh3foeyQ9WUyaiG0UQ9haMoHNktNB2"
BASE_URL = "https://api.harvestapi.io"

headers = {"X-API-Key": API_KEY}

# Test con url correcto
url = f"{BASE_URL}/linkedin/profile"

# Intento 1: url param
params = {"url": "https://www.linkedin.com/in/satyanadella"}
resp = requests.get(url, headers=headers, params=params, timeout=15)
print(f"Con url= Status: {resp.status_code}")
data = resp.json()
print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
