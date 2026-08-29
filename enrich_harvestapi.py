"""
enrich_harvestapi.py
====================
Con 2 llaves de HarvestAPI en rotación (Key 1 y Key 2).
Soporta $0.0064/perfil (Full Profile).

Extrae y actualiza metadata en Supabase/local:
  - country, city, country_code (desde HarvestAPI location)
  - harvest_company, harvest_position (cargo/empresa actuales verificados)
  - harvest_enriched: True (flag de procesado)
"""

import os
import sys
import time
import json
import argparse
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Fix Unicode para terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

KEYS = [
    os.getenv("HARVEST_API_KEY"),
    os.getenv("HARVEST_API_KEY_2")
]
# Filtrar None o vacías
KEYS = [k for k in KEYS if k]

HARVEST_BASE_URL = "https://api.harvestapi.io"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

COST_PER_CALL = 0.0064
BUDGET = 40.00  # $20 per key x 2 keys
MAX_PROFILES = int(BUDGET / COST_PER_CALL)

SLEEP_BETWEEN = 1.0  # 1s entre llamadas distribuyendo rotación

PRIORITY_KEYWORDS = [
    "pay", "payment", "pago", "stripe", "clip", "conekta", "oxxo", "openpay",
    "kushki", "mercado pago", "bancomer", "bbva", "banamex", "hsbc", "santander",
    "fintech", "finance", "financial", "banco", "bank", "banking", "credit",
    "credito", "lending", "loan", "remittance", "remesa", "transfer", "wire",
    "cross-border", "cross border", "forex", "fx", "exchange", "divisas",
    "wallet", "digital wallet", "crypto", "blockchain", "defi", "neobank",
    "starpago", "visa", "mastercard", "amex", "american express",
    "prosa", "e-global", "eglobal", "pagomovil", "cobro", "cobranza",
    "treasury", "tesoreria", "adquirencia", "acquiring", "pos", "punto de venta",
    "paytech", "wex", "flywire", "payoneer", "rappi", "nubank", "bnamerican",
    "mexico", "latam", "latinoamerica", "latin america"
]


def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] Faltan variables de Supabase en .env")
        sys.exit(1)
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def score_profile(row: dict) -> int:
    text = (
        (row.get("current_company") or "") + " " +
        (row.get("current_position") or "") + " " +
        str((row.get("metadata") or {}).get("full_name", ""))
    ).lower()

    score = 0
    for kw in PRIORITY_KEYWORDS:
        if kw in text:
            score += 1
    return score


def fetch_all_profiles(supabase: Client) -> dict:
    print("[INFO] Descargando perfiles pendientes de Supabase...")
    rows = []
    offset = 0
    PAGE = 1000
    while True:
        r = (
            supabase.table("connections")
            .select("id, linkedin_url, current_company, current_position, metadata")
            .neq("linkedin_url", "")
            .not_.is_("linkedin_url", None)
            .range(offset, offset + PAGE - 1)
            .execute()
        )
        batch = r.data or []
        rows.extend(batch)
        if len(batch) < PAGE:
            break
        offset += PAGE

    grouped = {}
    for row in rows:
        meta = row.get("metadata") or {}
        if meta.get("harvest_enriched"):
            continue
            
        url = row["linkedin_url"]
        if url not in grouped:
            grouped[url] = {"ids": [], "row": row, "score": score_profile(row)}
        grouped[url]["ids"].append(row["id"])
    
    sorted_urls = sorted(grouped.keys(), key=lambda x: grouped[x]["score"], reverse=True)
    return {url: grouped[url] for url in sorted_urls[:MAX_PROFILES]}


def call_harvest_rotated(linkedin_url: str, call_index: int) -> dict | None:
    if not KEYS:
        print("   [ERROR] No hay llaves de HarvestAPI en .env")
        return None

    # Rotación simple Round-Robin entre las llaves configuradas
    api_key = KEYS[call_index % len(KEYS)]
    key_label = f"Key {(call_index % len(KEYS)) + 1}"

    try:
        r = requests.get(
            f"{HARVEST_BASE_URL}/linkedin/profile",
            headers={"X-API-Key": api_key},
            params={"url": linkedin_url},
            timeout=20,
        )
        if r.status_code == 200:
            res_json = r.json()
            print(f"   [{key_label} OK]", end="")
            return res_json.get("element")
        else:
            print(f"   [{key_label} HTTP {r.status_code}] {r.text[:100]}")
            return None
    except Exception as e:
        print(f"   [{key_label} ERROR] {e}")
        return None


def build_metadata_update(existing_meta: dict, element: dict) -> dict:
    updated = dict(existing_meta or {})

    location = element.get("location") or {}
    parsed = location.get("parsed") or {}

    country = parsed.get("country") or parsed.get("countryFull") or ""
    country_code = location.get("countryCode") or ""
    city = parsed.get("city") or ""
    state = parsed.get("state") or ""
    linkedin_loc = location.get("linkedinText") or ""

    if country:
        updated["country"] = country
    if country_code:
        updated["country_code"] = country_code
    if city:
        updated["city"] = city
    if state:
        updated["state"] = state
    if linkedin_loc:
        updated["location_text"] = linkedin_loc

    positions = element.get("currentPosition") or []
    if positions:
        pos = positions[0]
        updated["harvest_company"] = pos.get("companyName") or ""
        updated["harvest_position"] = pos.get("position") or ""

    if element.get("headline"):
        updated["headline"] = element["headline"]

    updated["harvest_enriched"] = True
    return updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Modo prueba")
    args = parser.parse_args()

    print("=" * 65)
    print(f"[*] HarvestAPI Multi-Key Enricher v3 - Radar Comercial")
    print(f"   Llaves activas: {len(KEYS)} | Presupuesto total: ${BUDGET:.2f} USD")
    print("=" * 65)

    if not KEYS:
        print("[ERROR] No se encontraron HARVEST_API_KEY ni HARVEST_API_KEY_2 en .env")
        return

    supabase = get_supabase()
    grouped_profiles = fetch_all_profiles(supabase)

    if not grouped_profiles:
        print("[INFO] No hay perfiles pendientes de enriquecimiento.")
        return

    enriched = 0
    skipped = 0
    spend = 0.0

    for i, (url, data) in enumerate(grouped_profiles.items(), 0):
        print(f"\n[{i+1}/{len(grouped_profiles)}] URL: {url}")

        if args.dry_run:
            print(f"   [DRY] {len(data['ids'])} registros asociados - Sin llamada API")
            enriched += 1
        else:
            element = call_harvest_rotated(url, i)

            if not element:
                print(f" -> Sin datos devueltos")
                skipped += 1
            else:
                for pid in data["ids"]:
                    resp = supabase.table("connections").select("metadata").eq("id", pid).single().execute()
                    existing_meta = resp.data.get("metadata") or {}
                    new_meta = build_metadata_update(existing_meta, element)
                    supabase.table("connections").update({"metadata": new_meta}).eq("id", pid).execute()

                enriched += 1
                spend += COST_PER_CALL
                print(f" -> Guardado en Supabase")

            print(f"   [$$] Gasto: ${spend:.4f} / Sólido restante: ${BUDGET - spend:.4f}")
            time.sleep(SLEEP_BETWEEN)

    print("\n" + "=" * 65)
    print(f"[OK] Perfiles enriquecidos: {enriched}")
    print(f"[--] Registros fallidos/omitidos: {skipped}")
    print(f"[$$] Gasto total estimado: ${spend:.4f} USD")
    print("=" * 65)


if __name__ == "__main__":
    main()
