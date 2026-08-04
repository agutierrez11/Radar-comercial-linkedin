"""
enrich_harvestapi_v2.py
=======================
Con $0.9936 de saldo en HarvestAPI ($0.0064/perfil = 155 perfiles max).
Estrategia: priorizar perfiles de empresas Fintech/Pagos/Cross-border.

Actualiza metadata JSONB con:
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

HARVEST_API_KEY = "PLoaTJMcDvVpKu085uNjWvjavIGYnphM"
HARVEST_BASE_URL = "https://api.harvestapi.io"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

COST_PER_CALL = 0.0064
BUDGET = 0.9936  # Cuenta nueva: $1 completo
MAX_PROFILES = int(BUDGET / COST_PER_CALL)  # 155 perfiles

SLEEP_BETWEEN = 1.3  # free tier: 1 concurrencia

# Palabras clave de prioridad: empresas fintech/pagos/cross-border
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
        print("[ERROR] Faltan variables en .env")
        sys.exit(1)
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def score_profile(row: dict) -> int:
    """Asigna score de prioridad: más keywords de pagos = más urgente."""
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


def fetch_all_profiles(supabase: Client) -> list:
    """Trae todos los perfiles con linkedin_url. Los sortea por prioridad."""
    print("[INFO] Descargando perfiles de Supabase...")
    rows = []
    offset = 0
    PAGE = 500
    while True:
        r = (
            supabase.table("connections")
            .select("id, first_name, last_name, current_company, current_position, linkedin_url, metadata")
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
        print(f"  Descargados: {len(rows)}...", end="\r")

    print(f"\n[INFO] {len(rows)} perfiles con URL de LinkedIn.")

    # Filtrar los que ya fueron enriquecidos
    pending = [r for r in rows if not (r.get("metadata") or {}).get("harvest_enriched")]
    print(f"[INFO] {len(pending)} sin enriquecer aún.")

    # Sortear por score (pagos primero)
    pending.sort(key=lambda x: score_profile(x), reverse=True)
    print(f"[INFO] Tomando top {MAX_PROFILES} por relevancia fintech/pagos...")
    return pending[:MAX_PROFILES]


def call_harvest(linkedin_url: str) -> dict | None:
    try:
        r = requests.get(
            f"{HARVEST_BASE_URL}/linkedin/profile",
            headers={"X-API-Key": HARVEST_API_KEY},
            params={"url": linkedin_url},
            timeout=20,
        )
        if r.status_code == 200:
            return r.json().get("element")
        else:
            print(f"   [HTTP {r.status_code}] {r.text[:150]}")
            return None
    except Exception as e:
        print(f"   [ERROR] {e}")
        return None


def build_metadata_update(existing_meta: dict, element: dict) -> dict:
    """Fusiona metadata existente con datos nuevos de HarvestAPI."""
    updated = dict(existing_meta or {})

    # Location
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

    # Empresa/cargo actuales verificados
    positions = element.get("currentPosition") or []
    if positions:
        pos = positions[0]
        updated["harvest_company"] = pos.get("companyName") or ""
        updated["harvest_position"] = pos.get("position") or ""

    # Otros datos útiles
    if element.get("headline"):
        updated["headline"] = element["headline"]

    updated["harvest_enriched"] = True

    return updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="No escribe en Supabase")
    args = parser.parse_args()

    print("=" * 60)
    print(f"[*] HarvestAPI Enricher v2 - Radar Comercial")
    print(f"   Presupuesto: ${BUDGET} | ${COST_PER_CALL}/perfil | Max: {MAX_PROFILES} perfiles")
    print(f"   Dry-run: {args.dry_run}")
    print("=" * 60)

    supabase = get_supabase()
    profiles = fetch_all_profiles(supabase)

    if not profiles:
        print("[INFO] No hay perfiles pendientes de enriquecimiento.")
        return

    enriched = 0
    skipped = 0
    spend = 0.0

    for i, profile in enumerate(profiles, 1):
        name = f"{profile.get('first_name','')} {profile.get('last_name','')}".strip()
        url = profile.get("linkedin_url", "")
        pid = profile.get("id")
        company = profile.get("current_company", "N/A")
        priority = score_profile(profile)

        print(f"\n[{i}/{len(profiles)}] {name} | {company} (score={priority})")
        print(f"   URL: {url}")

        if args.dry_run:
            print(f"   [DRY] Perfil seleccionado - NO se llama a la API")
            enriched += 1
        else:
            element = call_harvest(url)

            if not element:
                print(f"   [--] Sin datos de API")
                skipped += 1
            else:
                existing_meta = profile.get("metadata") or {}
                new_meta = build_metadata_update(existing_meta, element)

                country = new_meta.get("country", "N/D")
                city = new_meta.get("city", "")
                h_company = new_meta.get("harvest_company", "")
                h_position = new_meta.get("harvest_position", "")

                print(f"   [LOC] {city}, {country}")
                print(f"   [JOB] {h_position[:60]} @ {h_company[:40]}")

                supabase.table("connections").update({"metadata": new_meta}).eq("id", pid).execute()

                enriched += 1
                spend += COST_PER_CALL

            print(f"   [$$] Gasto: ${spend:.4f} / ${BUDGET:.4f} restante: ${BUDGET - spend:.4f}")
            time.sleep(SLEEP_BETWEEN)

    print("\n" + "=" * 60)
    print(f"[OK] Enriquecidos: {enriched}")
    print(f"[--] Skipped:     {skipped}")
    print(f"[$$] Gasto total: ${spend:.4f} USD")
    print(f"[$$] Saldo aprox: ${BUDGET - spend:.4f} USD")
    print("=" * 60)


if __name__ == "__main__":
    main()
