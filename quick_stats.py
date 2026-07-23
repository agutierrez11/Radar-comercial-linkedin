"""
quick_stats.py — Radar Comercial
Genera datos duros desde el ZIP de LinkedIn para pasar al científico de datos.
"""
import os, zipfile, csv, io, re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

ZIP_PATH = r"C:\Users\Antonio\OneDrive\Downloads\Complete_LinkedInDataExport_07-05-2026.zip.zip"

# ── helpers ──────────────────────────────────────────────────────────────────

def normalize(text):
    if not text: return ""
    text = text.lower().strip()
    for src, dst in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        text = text.replace(src, dst)
    return text

def infer_country(email, company, position):
    email = (email or "").lower()
    blob = normalize(f"{company} {position}")
    if email.endswith(".mx"): return "México"
    if email.endswith(".cl"): return "Chile"
    if email.endswith(".co"): return "Colombia"
    if email.endswith(".pe"): return "Perú"
    if email.endswith(".br"): return "Brasil"
    if email.endswith(".ar"): return "Argentina"
    if re.search(r'\b(mexico|cdmx|monterrey|guadalajara|cancun|queretaro)\b', blob): return "México"
    if re.search(r'\b(chile|santiago)\b', blob): return "Chile"
    if re.search(r'\b(colombia|bogota|medellin)\b', blob): return "Colombia"
    if re.search(r'\b(peru|lima)\b', blob): return "Perú"
    if re.search(r'\b(brasil|brazil|sao paulo|rio)\b', blob): return "Brasil"
    if re.search(r'\b(argentina|buenos aires|cordoba)\b', blob): return "Argentina"
    if re.search(r'\b(espana|spain|madrid|barcelona)\b', blob): return "España"
    if re.search(r'\b(usa|united states|new york|san francisco|chicago)\b', blob): return "USA"
    return "Desconocido"

def infer_hierarchy(position):
    p = normalize(position)
    if re.search(r'\b(ceo|cfo|cto|cmo|cro|coo|founder|fundador|cofounder|director general|managing director|presidente)\b', p):
        return "C-Level"
    if re.search(r'\b(director|head|vp|vice president|vicepresidente)\b', p):
        return "Director"
    if re.search(r'\b(gerente|manager|jefe|responsable|lead)\b', p):
        return "Gerente"
    if re.search(r'\b(student|estudiante|freelance|independiente|desempleado)\b', p):
        return "Sin valor comercial"
    return "Otros"

def infer_sector(position, company):
    blob = normalize(f"{position} {company}")
    if re.search(r'\b(fintech|pago|cobro|treasury|tesoreria|banking|bank|banco|credito|credit|adquirente|pos|terminal)\b', blob): return "Fintech/Pagos"
    if re.search(r'\b(retail|ecommerce|tienda|store|marketplace|comercio electronico)\b', blob): return "Retail/eCommerce"
    if re.search(r'\b(software|saas|tech|platform|developer|engineer|startup|digital)\b', blob): return "SaaS/Tech"
    if re.search(r'\b(manufactura|industrial|planta|supply chain|logistic|transport)\b', blob): return "Manufactura/Logística"
    if re.search(r'\b(health|salud|pharma|hospital|medico|clinica)\b', blob): return "Salud"
    if re.search(r'\b(educacion|universidad|school|edtech|instituto)\b', blob): return "Educación"
    if re.search(r'\b(gobierno|gobierno|municipal|federal|secretaria|publico)\b', blob): return "Gobierno"
    if re.search(r'\b(consulting|consultor|advisory|strategy|consultoria)\b', blob): return "Consultoría"
    if re.search(r'\b(media|marketing|publicidad|advertising|agencia|agency)\b', blob): return "Marketing/Media"
    return "Otro"

def is_purge_candidate(row, connected_years_threshold=4):
    company   = (row.get("Company","") or "").strip()
    position  = (row.get("Position","") or "").strip()
    name      = (row.get("First Name","") or "").strip() + " " + (row.get("Last Name","") or "").strip()
    name      = name.strip()
    connected = (row.get("Connected On","") or "").strip()
    
    reasons = []
    if not company:             reasons.append("Sin empresa")
    if not position:            reasons.append("Sin cargo")
    if len(name) < 4:           reasons.append("Nombre incompleto")
    if re.search(r'\b(student|estudiante|desempleado|unemployed)\b', normalize(position)):
        reasons.append("Cargo genérico sin valor")
    if connected:
        try:
            dt = datetime.strptime(connected, "%d %b %Y")
            if (datetime.now() - dt).days > connected_years_threshold * 365:
                reasons.append(f"Conexión >{ connected_years_threshold} años sin actividad")
        except: pass
    
    return reasons  # empty = no purge candidate

# ── main ─────────────────────────────────────────────────────────────────────

def run():
    if not os.path.exists(ZIP_PATH):
        print(f"❌  ZIP no encontrado en: {ZIP_PATH}")
        return

    contacts   = []
    positions  = []
    owner_name = "Desconocido"

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        files = z.namelist()
        print(f"📦  Archivos en ZIP: {', '.join(files)}\n")

        # ── Profile ──
        if "Profile.csv" in files:
            with z.open("Profile.csv") as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="ignore"))
                for row in reader:
                    fn = row.get("First Name","")
                    ln = row.get("Last Name","")
                    owner_name = f"{fn} {ln}".strip()
                    break

        # ── Positions ──
        if "Positions.csv" in files:
            with z.open("Positions.csv") as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="ignore"))
                for row in reader:
                    positions.append({
                        "company": row.get("Company Name",""),
                        "title":   row.get("Title",""),
                        "start":   row.get("Started On",""),
                        "end":     row.get("Finished On",""),
                    })

        # ── Connections ──
        conn_file = next((f for f in files if "Connection" in f), None)
        if conn_file:
            with z.open(conn_file) as f:
                # Skip non-data header rows LinkedIn adds
                raw = io.TextIOWrapper(f, encoding="utf-8", errors="ignore")
                lines = raw.readlines()
                # Find the real CSV header row
                start_idx = next((i for i, l in enumerate(lines) if "First Name" in l), 0)
                reader = csv.DictReader(lines[start_idx:])
                for row in reader:
                    country   = infer_country(row.get("Email Address",""), row.get("Company",""), row.get("Position",""))
                    hierarchy = infer_hierarchy(row.get("Position",""))
                    sector    = infer_sector(row.get("Position",""), row.get("Company",""))
                    purge_r   = is_purge_candidate(row)
                    contacts.append({
                        "name":      f"{row.get('First Name','')} {row.get('Last Name','')}".strip(),
                        "company":   row.get("Company",""),
                        "position":  row.get("Position",""),
                        "email":     row.get("Email Address",""),
                        "connected": row.get("Connected On",""),
                        "country":   country,
                        "hierarchy": hierarchy,
                        "sector":    sector,
                        "purge_reasons": purge_r,
                        "is_purge_candidate": len(purge_r) > 0,
                    })

    # ─────────────────────────────────────────────────────────────────────────
    # REPORT
    # ─────────────────────────────────────────────────────────────────────────
    total = len(contacts)
    hier_counts = Counter(c["hierarchy"] for c in contacts)
    country_counts = Counter(c["country"] for c in contacts)
    sector_counts  = Counter(c["sector"]  for c in contacts)
    purge_candidates = [c for c in contacts if c["is_purge_candidate"]]
    clase_a = [c for c in contacts if c["hierarchy"] in ("C-Level","Director") and c["country"] != "Desconocido"]

    print("=" * 60)
    print(f"  RADAR COMERCIAL — Datos Duros de {owner_name}")
    print("=" * 60)

    print(f"\n📊  RED TOTAL: {total:,} contactos")

    print(f"\n👑  JERARQUÍA:")
    for h in ["C-Level","Director","Gerente","Otros","Sin valor comercial"]:
        n = hier_counts.get(h, 0)
        pct = n/total*100 if total else 0
        print(f"    {h:<25} {n:>5,}  ({pct:.1f}%)")

    print(f"\n🌎  TOP 10 PAÍSES:")
    for country, n in country_counts.most_common(10):
        pct = n/total*100
        print(f"    {country:<25} {n:>5,}  ({pct:.1f}%)")

    print(f"\n🏭  TOP 10 SECTORES:")
    for sector, n in sector_counts.most_common(10):
        pct = n/total*100
        print(f"    {sector:<25} {n:>5,}  ({pct:.1f}%)")

    print(f"\n📅  HISTORIAL DE POSICIONES ({len(positions)} registros):")
    for p in positions[:10]:
        end_label = p['end'] if p['end'] else "Actual"
        print(f"    {p['start'][:7] if p['start'] else '?'} → {end_label[:7] if end_label != 'Actual' else 'Actual'}  |  {p['title']} @ {p['company']}")

    print(f"\n🗑️   CANDIDATOS A PURGA: {len(purge_candidates):,} / {total:,}  ({len(purge_candidates)/total*100:.1f}%)")
    purge_reason_counts = Counter(r for c in purge_candidates for r in c["purge_reasons"])
    for reason, n in purge_reason_counts.most_common():
        print(f"    {reason:<40} {n:>5,}")

    print(f"\n⚠️  DISCLAIMER (para el científico de datos):")
    print(f"    LinkedIn no diferencia contactos de valor informacional de los comerciales.")
    print(f"    Algunos contactos marcados como 'purga' pueden ser fuentes de conocimiento,")
    print(f"    playbooks o alianzas estratégicas. REVISAR PERFIL ANTES DE ELIMINAR.")

    print(f"\n🎯  CLASE A (C-Level + Director + País identificado): {len(clase_a):,}")
    print(f"    Dunbar Layer óptima:                              150")
    print(f"    Excedente sobre Dunbar:                          {max(0, len(clase_a)-150):,}")

    # ── CSV output ──
    out_path = os.path.join(os.path.dirname(ZIP_PATH), "radar_datos_duros.csv")
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        fieldnames = ["name","company","position","email","connected","country","hierarchy","sector","is_purge_candidate","purge_reasons"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in contacts:
            row = {k: c.get(k,"") for k in fieldnames}
            row["purge_reasons"] = " | ".join(c["purge_reasons"])
            writer.writerow(row)
    print(f"\n✅  CSV exportado: {out_path}")
    print("=" * 60)

if __name__ == "__main__":
    run()
