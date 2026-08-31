import json
import re
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        with open('enriched_connections.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        with open('master_data.js', 'r', encoding='utf-8') as f:
            js = f.read()
        m = re.search(r'window\.MASTER_CONNECTIONS_DATA\s*=\s*(\[.*?\]);', js, re.DOTALL)
        if not m:
            print("❌ No se encontró la base de datos de contactos.")
            return
        data = json.loads(m.group(1))

    total = len(data)
    print("=" * 60)
    print(f"🧠 ANÁLISIS DE SEGMENTACIÓN CONDUCTUAL DE BÓVEDA ({total:,} CONTACTOS)")
    print("=" * 60)

    c_level = []
    directors = []
    managers = []
    others = []

    for c in data:
        pos = (c.get('position') or '').lower()
        hier = c.get('hierarchy') or ''
        if hier == 'C-Level' or any(k in pos for k in ['ceo', 'chief', 'founder', 'socio', 'vp']):
            c_level.append(c)
        elif hier == 'Director' or 'director' in pos or 'head' in pos:
            directors.append(c)
        elif hier == 'Gerente' or 'gerente' in pos or 'manager' in pos or 'lead' in pos:
            managers.append(c)
        else:
            others.append(c)

    print(f"👑 Clúster 1 - C-Level / Fundadores (Decisores de Alto Nivel): {len(c_level):,} ({len(c_level)/total*100:.1f}%)")
    print(f"🎯 Clúster 2 - Directores / Heads (Influenciadores Estratégicos): {len(directors):,} ({len(directors)/total*100:.1f}%)")
    print(f"⚙️ Clúster 3 - Gerentes / Leads (Compradores Operativos): {len(managers):,} ({len(managers)/total*100:.1f}%)")
    print(f"👥 Clúster 4 - Especialistas / Otros (Contactos de Soporte): {len(others):,} ({len(others)/total*100:.1f}%)")
    print("-" * 60)

    # Email readiness
    with_email = [c for c in data if c.get('email')]
    with_dms = [c for c in data if (c.get('msg_count') or 0) > 0]

    print(f"✉️ Contactos con Email Directo Registrado: {len(with_email):,}")
    print(f"💬 Contactos con Historial de DMs Activo: {len(with_dms):,}")
    print("=" * 60)
    print("✅ Segmentación completada. Lista para exportar o prospectar.")

if __name__ == "__main__":
    main()
