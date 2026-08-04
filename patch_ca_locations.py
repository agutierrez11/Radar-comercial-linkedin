import json
from enrich_and_normalize_connections import infer_location_and_status, infer_seniority

def patch_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Could not load {filename}: {e}")
        return

    updates = 0
    for p in data:
        # Re-run the inference
        first = p.get('first_name', '') or ''
        last = p.get('last_name', '') or ''
        comp = p.get('company', '') or ''
        pos = p.get('position', '') or p.get('position_current', '') or ''
        conn = p.get('connected_on', '') or ''
        
        loc_info = infer_location_and_status(first, last, comp, pos, conn)
        
        current_seniority = p.get('seniority')
        new_seniority = infer_seniority(pos)
        if current_seniority != new_seniority:
            p['seniority'] = new_seniority
            updates += 1
            
        current_country = p.get('country') or "Desconocido"
        if current_country == "Desconocido" and loc_info['country'] != "Desconocido":
            p['country'] = loc_info['country']
            p['city'] = loc_info['city']
            p['lat'] = loc_info['lat']
            p['lng'] = loc_info['lng']
            updates += 1
        elif current_country not in loc_info['country'] and loc_info['country'] != "Desconocido":
            p['country'] = loc_info['country']
            p['city'] = loc_info['city']
            p['lat'] = loc_info['lat']
            p['lng'] = loc_info['lng']
            updates += 1
            
    if updates > 0:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Patched {updates} records in {filename}")
    else:
        print(f"No updates needed for {filename}")

patch_json('enriched_connections.json')
patch_json('master_data.json')
