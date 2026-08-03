"""
upload_enriched_data.py
Sube enriched_connections.json a Supabase en lotes.
- Crea el seller 'Antonio' si no existe.
- Normaliza campos para la tabla connections.
- Almacena todo el JSON original en metadata (JSONB).
"""
import json
import os
import unicodedata
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ENRICHED_FILE = os.path.join(os.path.dirname(__file__), "enriched_connections.json")
SELLER_NAME = "Antonio Gutierrez"
SELLER_EMAIL = "antonio@radarcomercial.app"
BATCH_SIZE = 100


def normalize(text: str) -> str:
    """Quita acentos y convierte a minusculas para busqueda exacta."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def get_or_create_seller(supabase: Client) -> str:
    res = supabase.table("sellers").select("id").eq("email", SELLER_EMAIL).execute()
    if res.data:
        seller_id = res.data[0]["id"]
        print(f"[INFO] Seller existente encontrado: {seller_id}")
        return seller_id
    res = supabase.table("sellers").insert({
        "name": SELLER_NAME,
        "email": SELLER_EMAIL,
    }).execute()
    seller_id = res.data[0]["id"]
    print(f"[INFO] Seller creado: {seller_id}")
    return seller_id


def load_connections() -> list:
    print(f"[INFO] Cargando {ENRICHED_FILE}...")
    with open(ENRICHED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[INFO] {len(data)} contactos cargados.")
    return data


def build_row(contact: dict, seller_id: str) -> dict:
    company = contact.get("company") or contact.get("company_zip") or ""
    position = contact.get("position_current") or contact.get("position") or contact.get("position_zip") or ""
    return {
        "seller_id": seller_id,
        "first_name": contact.get("first_name", ""),
        "last_name": contact.get("last_name", ""),
        "current_company": company,
        "current_position": position,
        "linkedin_url": contact.get("url", ""),
        "normalized_company": normalize(company),
        "metadata": {
            "job_status": contact.get("job_status", ""),
            "audit_status": contact.get("audit_status", ""),
            "sentiment": contact.get("sentiment", ""),
            "intent": contact.get("intent", ""),
            "has_reply": contact.get("has_reply", False),
            "is_deal": contact.get("is_deal", False),
            "is_friendly": contact.get("is_friendly", False),
            "is_they_selling": contact.get("is_they_selling", False),
            "turns": contact.get("turns", 0),
            "direction": contact.get("direction", ""),
            "last_post_date": contact.get("last_post_date", ""),
            "last_post_text": contact.get("last_post_text", ""),
            "last_updated_apify": contact.get("last_updated_apify", ""),
            "connected_on": contact.get("connected_on", ""),
            "full_name": contact.get("full_name", ""),
        }
    }


def upload_in_batches(supabase: Client, rows: list):
    total = len(rows)
    uploaded = 0
    errors = 0
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        try:
            supabase.table("connections").insert(batch).execute()
            uploaded += len(batch)
            pct = (uploaded / total) * 100
            print(f"[OK] {uploaded}/{total} ({pct:.1f}%) subidos...", end="\r")
        except Exception as e:
            errors += len(batch)
            print(f"\n[ERROR] Lote {i}-{i+len(batch)} fallido: {e}")
    print(f"\n[DONE] Carga completada: {uploaded} exito, {errors} errores de {total} total.")


def main():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env")
        sys.exit(1)

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    seller_id = get_or_create_seller(supabase)
    contacts = load_connections()
    rows = [build_row(c, seller_id) for c in contacts]
    print(f"[INFO] Iniciando carga de {len(rows)} filas en lotes de {BATCH_SIZE}...")
    upload_in_batches(supabase, rows)


if __name__ == "__main__":
    main()
