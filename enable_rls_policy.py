"""
enable_rls_policy.py
Habilita la politica RLS de lectura publica en la tabla 'connections'
usando la Supabase Management API.
"""
import urllib.request, json, ssl, sys, os

SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
PROJECT_REF = "hsrseeqhdtogpdqbveay"
SUPA_URL = f"https://{PROJECT_REF}.supabase.co"

ctx = ssl.create_default_context()

# El endpoint correcto para ejecutar SQL en Supabase es via postgREST
# pero para DDL necesitamos el Management API o el SQL Editor endpoint
# Supabase Management API: https://api.supabase.com/v1/projects/{ref}/database/query

sql_query = (
    "ALTER TABLE public.connections ENABLE ROW LEVEL SECURITY; "
    "DO $$ BEGIN "
    "IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename='connections' AND policyname='Public read access') "
    "THEN CREATE POLICY \"Public read access\" ON public.connections FOR SELECT TO anon, authenticated USING (true); "
    "END IF; END $$;"
)

# Intentar via Management API
mgmt_url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"
payload = json.dumps({"query": sql_query}).encode("utf-8")

req = urllib.request.Request(mgmt_url, data=payload, method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("Authorization", f"Bearer {SERVICE_KEY}")

try:
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        print("Status:", r.status)
        result = r.read().decode("utf-8")
        print("Result:", result[:500])
        sys.exit(0)
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")
    print(f"HTTP {e.code}:", body[:500])

# Si falla Management API, intentar via endpoint rpc de postgREST
# Esto solo funciona si hay una funcion SQL publica
print("\nIntentando via SQL directo con service key...")

# Supabase permite ejecutar SQL raw via https://PROJECT.supabase.co/rest/v1/rpc/
# Pero necesitamos una funcion. Alternativa: usar el endpoint pg
pg_url = f"{SUPA_URL}/pg/query"
req2 = urllib.request.Request(pg_url, data=payload, method="POST")
req2.add_header("Content-Type", "application/json")
req2.add_header("apikey", SERVICE_KEY)
req2.add_header("Authorization", f"Bearer {SERVICE_KEY}")

try:
    with urllib.request.urlopen(req2, context=ctx, timeout=30) as r:
        print("PG Status:", r.status)
        print("PG Result:", r.read().decode("utf-8")[:500])
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")
    print(f"PG HTTP {e.code}:", body[:300])
    print("\nACCION MANUAL REQUERIDA:")
    print("Ir a: https://app.supabase.com/project/hsrseeqhdtogpdqbveay/editor")
    print("Ejecutar este SQL:")
    print(sql_query)
