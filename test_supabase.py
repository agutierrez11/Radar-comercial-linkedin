import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Usamos la Service Role Key para tener permisos de escritura sin RLS
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

async def test_connection():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[ERROR] Faltan las variables SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en el .env")
        return

    print("[INFO] Conectando a Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Intentamos leer la tabla de sellers para validar conexión
        response = supabase.table("sellers").select("*").limit(1).execute()
        print("[OK] Conexion exitosa. Base de datos operativa.")
        print(f"Respuesta de prueba: {response.data}")
    except Exception as e:
        print(f"[ERROR] Error al conectar o consultar Supabase: {e}")
        print("Asegurate de haber ejecutado el script SQL en el dashboard de Supabase primero!")

if __name__ == "__main__":
    asyncio.run(test_connection())
