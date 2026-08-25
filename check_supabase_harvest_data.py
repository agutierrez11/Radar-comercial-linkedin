import os, requests, json

url = "https://hsrseeqhdtogpdqbveay.supabase.co"
key = os.environ.get("SUPABASE_KEY")
if not key and os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('SUPABASE_KEY=') or line.startswith('SUPABASE_ANON_KEY='):
                key = line.split('=', 1)[1].strip().strip('"')

print(f"Supabase Key found: {key[:20]}..." if key else "No Key")

if key:
    headers = {'apikey': key, 'Authorization': f'Bearer {key}'}
    # Count rows in connections table on hsrseeqhdtogpdqbveay
    try:
        r = requests.get(f"{url}/rest/v1/connections?select=count", headers=headers)
        print("Count response status:", r.status_code, "Header Range:", r.headers.get('Content-Range'))
        
        # Check sample metadata for harvest_enriched
        r2 = requests.get(f"{url}/rest/v1/connections?select=id,first_name,last_name,metadata&limit=10", headers=headers)
        data = r2.json()
        print(f"Fetched {len(data)} rows from Supabase connections table.")
        if len(data) > 0:
            print("Sample row 0 metadata:", data[0].get('metadata'))
    except Exception as e:
        print("Error querying Supabase:", e)
