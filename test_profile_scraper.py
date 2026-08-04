import os
import json
import urllib.request
import urllib.error
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

def load_env():
    env = {}
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def main():
    print("=== TEST APIFY LINKEDIN PROFILE SCRAPER (ZERO-WASTE) ===")
    
    env_vars = load_env()
    token = env_vars.get("APIFY_API_TOKEN")
    
    if not token:
        print("[!] ERROR: APIFY_API_TOKEN not found.")
        return
        
    test_profile = "https://www.linkedin.com/in/williamhgates"
    print(f"Testing profile: {test_profile}")
    
    # Using the standard bebity profile scraper for full profile extraction
    payload = {
        "urls": [test_profile],
        "minDelay": 1,
        "maxDelay": 5
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    
    # We use bebity/linkedin-profile-scraper
    actor_id = "harvestapi~linkedin-profile-scraper"
    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items?token={token}"
    
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )
    
    print("Running scraper synchronously on Apify. This will take ~1 minute...")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_body = response.read().decode("utf-8")
            items = json.loads(res_body)
            
            if not items:
                print("No data returned!")
            else:
                profile = items[0]
                print("\n[+] SUCCESS! Data extracted:")
                print(f"Name: {profile.get('firstName')} {profile.get('lastName')}")
                print(f"Headline: {profile.get('headline')}")
                print(f"Location: {profile.get('location')}")
                print(f"Industry: {profile.get('industry')}")
                
                # Save raw JSON for inspection
                with open('test_profile_raw.json', 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2, ensure_ascii=False)
                print("\nFull raw JSON saved to 'test_profile_raw.json' for analysis.")
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
