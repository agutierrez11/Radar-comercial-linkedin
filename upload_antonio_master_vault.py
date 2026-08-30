import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://hsrseeqhdtogpdqbveay.supabase.co").strip('"')
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip('"')
VAULT_ID = "vault_antonio"


headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def post_data(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return True
    except urllib.error.HTTPError as e:
        print(f"Error on {table}: {e.code} {e.reason} -> {e.read().decode('utf-8-sig', errors='ignore')}")
        return False
    except Exception as e:
        print(f"Error on {table}: {e}")
        return False

def main():
    print("[SUPABASE] Uploading Antonio Master Vault to Supabase...")
    
    # 1. Upsert Vault
    vault_payload = [{
        "id": VAULT_ID,
        "owner_id": "antonio",
        "owner_name": "Antonio Gutierrez",
        "status": "active",
        "contacts_count": 2953
    }]
    headers["Prefer"] = "resolution=merge-duplicates"
    post_data("vaults", vault_payload)
    print("SUCCESS: Vault record created/updated: vault_antonio")
    
    # 2. Load contacts
    with open("enriched_connections.json", "r", encoding="utf-8") as f:
        raw_contacts = json.load(f)
    
    active_contacts = [c for c in raw_contacts if c.get("crmStatus") != "Descartado" and not c.get("discardedFromPurge") and c.get("audit_status") != "discarded"]
    print(f"Processing {len(active_contacts)} active contacts...")
    
    contacts_payload = []
    for c in active_contacts:
        c_id = str(c.get("id") or c.get("url") or c.get("name"))
        contacts_payload.append({
            "id": f"{VAULT_ID}_c_{c_id}",
            "vault_id": VAULT_ID,
            "name": c.get("name") or c.get("full_name") or f"{c.get('first_name', '')} {c.get('last_name', '')}".strip() or "Contacto",
            "first_name": c.get("first_name", ""),
            "last_name": c.get("last_name", ""),
            "company": c.get("company", ""),
            "position": c.get("position", ""),
            "country": c.get("country", ""),
            "city": c.get("city", ""),
            "url": c.get("url", ""),
            "email": c.get("email", ""),
            "score": c.get("score", 50),
            "crm_status": c.get("crmStatus", "Ninguno"),
            "audit_status": c.get("audit_status", "verified"),
            "job_status": c.get("job_status", "active"),
            "metadata": {
                "apify_verified": bool(c.get("last_updated_apify")),
                "harvest_enriched": bool(c.get("harvest_status")),
                "original_company": c.get("originalCompany") or c.get("company_zip"),
                "original_position": c.get("originalPosition") or c.get("position_zip")
            }
        })
    
    # Upload contacts in chunks of 500
    chunk_size = 500
    for i in range(0, len(contacts_payload), chunk_size):
        chunk = contacts_payload[i:i+chunk_size]
        ok = post_data("contacts", chunk)
        if ok:
            print(f"  Uploaded contacts {i+1} to {min(i+chunk_size, len(contacts_payload))}...")

    # 3. Upload Positions
    positions = [
        {"vault_id": VAULT_ID, "company": "Clip", "title": "Head of Enterprise Sales", "start_date": "2023", "end_date": "Presente", "location": "Ciudad de Mexico"},
        {"vault_id": VAULT_ID, "company": "Fiserv", "title": "Senior Commercial Director", "start_date": "2021", "end_date": "2023", "location": "Ciudad de Mexico"},
        {"vault_id": VAULT_ID, "company": "LATAM Commerce", "title": "VP of Revenue & Partnerships", "start_date": "2019", "end_date": "2021", "location": "Ciudad de Mexico"},
        {"vault_id": VAULT_ID, "company": "ENFA", "title": "Director de Desarrollo Comercial", "start_date": "2017", "end_date": "2019", "location": "Ciudad de Mexico"},
        {"vault_id": VAULT_ID, "company": "JTI (Japan Tobacco International)", "title": "Key Account Manager B2B", "start_date": "2015", "end_date": "2017", "location": "Ciudad de Mexico"},
        {"vault_id": VAULT_ID, "company": "Conagra Brands", "title": "Gerente de Cuentas Clave", "start_date": "2013", "end_date": "2015", "location": "Ciudad de Mexico"}
    ]
    post_data("positions", positions)
    print("SUCCESS: Uploaded 6 career positions")
    
    print("SUCCESS: ANTONIO MASTER VAULT UPLOAD COMPLETE!")

if __name__ == "__main__":
    main()
