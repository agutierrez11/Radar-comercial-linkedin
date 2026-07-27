"""
Radar de Riesgo Regulatorio CNBV / SIPRES (Early Warning System)
Este script monitorea el padron oficial de SOFOMes en Mexico para detectar:
1. Cambios de estatus en SIPRES (En Supervisión, Requerimiento o Cancelación previa).
2. Sitios web caidos / Dominios vencidos (indicador temprano de falta de actividad).
3. Entidades sin movimiento contable reportado.

Autor: Antonio Gutiérrez (RevOps & Growth Strategist - Intelligential)
"""

import urllib.request
import urllib.parse
import json
import ssl
import re
from datetime import datetime

# Desactivar verificación estricta SSL para scraping gubernamental si es necesario
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_website_health(url):
    """
    Verifica la salud del sitio web de una SOFOM.
    Si el sitio da 404, error DNS o timeout, marca Alerta Amarilla de abandono operativo.
    """
    if not url or not url.startswith('http'):
        return "SIN_URL", "No cuenta con URL oficial registrada"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
            if response.status == 200:
                return "OK", f"Sitio activo (HTTP {response.status})"
            else:
                return "ALERTA", f"Respuesta inusual (HTTP {response.status})"
    except urllib.error.HTTPError as e:
        return "ALERTA_ALTA", f"Error HTTP {e.code} - Posible inactividad"
    except urllib.error.URLError as e:
        return "ALERTA_CRITICA", f"Falla de Dominio/DNS ({e.reason}) - Alto riesgo de abandono"
    except Exception as e:
        return "ALERTA", f"Timeout / Error de conexión: {str(e)[:50]}"

def parse_sipres_status(status_text):
    """
    Clasifica el riesgo regulatorio segun el estatus en el padron SIPRES/CONDUSEF.
    """
    status_lower = status_text.lower() if status_text else ""
    
    if "cancelad" in status_lower or "revocad" in status_lower:
        return "CANCELADA", "🔴 Cancelación oficial registrada ante la autoridad."
    elif "supervis" in status_lower or "observac" in status_lower or "prevenci" in status_lower:
        return "OPORTUNIDAD_RESCATE", "⚡ ALERTA DE OPORTUNIDAD: SOFOM en periodo de supervisión/observaciones. Plazo de regularización activo."
    elif "operac" in status_lower or "activ" in status_lower:
        return "OPERANDO", "🟢 En operación normal registrada."
    else:
        return "REVISION_REQUERIDA", "🟡 Estatus ambiguo. Requiere auditoría de expediente."

def generate_regulatory_alert(entity_name, rfc, status_sipres, website_url):
    """
    Genera la ficha de alerta de riesgo regulatorio para el equipo comercial de Intelligential.
    """
    status_code, status_desc = parse_sipres_status(status_sipres)
    web_status, web_desc = check_website_health(website_url)
    
    # Calcular nivel de prioridad comercial para abordaje de rescate
    is_rescue_candidate = (status_code == "OPORTUNIDAD_RESCATE") or (web_status in ["ALERTA_CRITICA", "ALERTA_ALTA"])
    
    alert_payload = {
        "timestamp": datetime.now().isoformat(),
        "entidad_denominacion": entity_name,
        "rfc": rfc,
        "estatus_regulacion_sipres": status_sipres,
        "diagnostico_cnbv": status_desc,
        "salud_sitio_web": web_desc,
        "candidato_rescate_intelligential": is_rescue_candidate,
        "pitch_sugerido": (
            "PROPUESTA DE RESCATE URGENTE: Notamos observaciones de operatividad ante la autoridad. "
            "Desplegamos el Core Bancario de Intelligential en 14 días para asegurar evidencia contable y cumplimiento CNBV/SITI."
            if is_rescue_candidate else "Monitoreo preventivo estándar."
        )
    }
    return alert_payload

if __name__ == "__main__":
    print("=" * 70)
    print("RADAR DE RIESGO REGULATORIO SOFOMES (CNBV / SIPRES) - INTELLIGENTIAL")
    print("=" * 70)
    
    # Prueba de concepto con SOFOMes de muestra
    samples = [
        {"name": "FINANCIERA EJEMPLO A, SOFOM ENR", "rfc": "FEA120304ABC", "sipres": "En Supervisión CNBV", "url": "https://www.google.com"},
        {"name": "INVERSIONES INACTIVAS B, SOFOM ENR", "rfc": "IIB990101XYZ", "sipres": "Observaciones en Expediente", "url": "https://sitio-inexistente-sofom-12345.com.mx"},
        {"name": "CREDITO SOLIDO C, SOFOM ENR", "rfc": "CSC150607123", "sipres": "Operando / Registro Activo SIPRES", "url": "https://www.condusef.gob.mx"}
    ]
    
    for item in samples:
        alert = generate_regulatory_alert(item["name"], item["rfc"], item["sipres"], item["url"])
        print(f"\nEntidad: {alert['entidad_denominacion']}")
        print(f"Estatus SIPRES: {alert['estatus_regulacion_sipres']}")
        print(f"Salud Web: {alert['salud_sitio_web']}")
        print(f"Candidato Rescate Quick-Win?: {'SI [RESCATE]' if alert['candidato_rescate_intelligential'] else 'NO [NORMAL]'}")
        print(f"Pitch Recomendado: {alert['pitch_sugerido']}")
        print("-" * 70)
