import json
import csv
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Inspect master_data.json or enriched_connections.json
try:
    with open("master_data.json", "r", encoding="utf-8") as f:
        master = json.load(f)
        print(f"master_data.json count: {len(master)}")
except Exception as e:
    print("master_data err:", e)

try:
    with open("radar_database_final.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"radar_database_final.csv count: {len(rows)}")
        # Check countries
        countries = set(r.get("Country", "") for r in rows)
        print(f"Paises unicos: {len(countries)}, Muestra: {list(countries)[:5]}")
except Exception as e:
    print("csv err:", e)

# Check index.html embedded data
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
        # Look for window.MASTER_DATA or similar
        matches = re.findall(r'(\d+)\s+contactos|(\d+)\s+conexiones', html)
        print(f"index.html size: {len(html)} bytes")
except Exception as e:
    print("index.html err:", e)
