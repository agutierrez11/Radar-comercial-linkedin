import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"
base_url = "https://zenmux.ai/api/v1"

# Check user balance endpoint
for ep in ["/user/balance", "/user/info", "/dashboard/billing/usage", "/models"]:
    try:
        r = requests.get(f"{base_url}{ep}", headers={"Authorization": f"Bearer {key}"}, timeout=4)
        print(f"{ep}: {r.status_code} -> {r.text[:150]}", flush=True)
    except Exception as e:
        print(f"{ep}: err {e}", flush=True)
