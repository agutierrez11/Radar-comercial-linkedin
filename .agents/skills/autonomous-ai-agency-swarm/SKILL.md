---
name: autonomous-ai-agency-swarm
description: Framework maestro para crear y orquestar una Agencia Digital de Agentes de IA Autónomos (basado en Agency Swarm, CrewAI y OpenCompany). Roles especializados, comunicación P2P y rendición de cuentas ejecutiva en español natural.
---

# Autonomous AI Agency Swarm — Framework de Agencia Digital de Agentes de IA

Esta habilidad define la arquitectura para crear, desplegar y operar una **Agencia Digital de Agentes de IA Autónomos**, donde múltiples agentes especializados trabajan como un equipo coordinado con roles claros, supervisión mutua y reportes diarios en lenguaje natural para el Director (Antonio).

---

## 🏛️ Estructura Orgánica de la Agencia Agéntica

```
                      👑 DIRECTOR / CE-CEO (Antonio)
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
[ 🎯 AGENTE SDR B2B ]    [ 🔬 AGENTE INTEL & RESEARCH ] [ 📊 AGENTE REVOPS & CRM ]
• Minería de leads       • Enriquecimiento de empresas   • Calificación de leads
• Redacción de DMs       • Detección de triggers         • Actualización de CRM
• Detección de puentes   • Análisis de competidores      • Reporte de métricas
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                    [ 🛡️ AGENTE QA & VERIFICACIÓN ]
                    • Previene alucinaciones y datos falsos
                    • Emite el Reporte Ejecutivo Diario en Español
```

---

## 🛠️ Roles Especializados & Protocolo de Trabajo

### 1. 🎯 Agente SDR B2B (Prospección & Outreach)
- **Misión:** Identificar perfiles ICP en LinkedIn/Web, detectar conexiones de 1er grado y redactar secuencias de mensajes sin fricción.
- **Herramientas:** `crawl4ai`, `harvestapi`, `llm_router`.

### 2. 🔬 Agente Intel & Market Research (Investigación Profunda)
- **Misión:** Analizar el stack tecnológico de los prospectos, detectar rondas de fondeo, cambios de directivos y noticias del sector.
- **Herramientas:** `search_web`, `read_url_content`, `osint-recon-arsenal`.

### 3. 📊 Agente RevOps & CRM (Inteligencia de Datos)
- **Misión:** Normalizar datos, eliminar duplicados, aplicar Scoring de conversión y sincronizar el estado del pipeline (`crmState`).
- **Herramientas:** `compai-crm`, `posthog-product-analytics`.

### 4. 🛡️ Agente QA & Reportes Ejecutivos (Comunicación Humana)
- **Misión:** Auditar las acciones de los otros 3 agentes, verificar que no existan datos inventados y enviar el **Standup Ejecutivo Diario** a Telegram/Slack en español claro y accesible.

---

## 💬 Formato del Standup Ejecutivo Diario (Lenguaje Natural)

```text
🤖 REPORT DIARIO DE LA AGENCIA AGÉNTICA

1. 🎯 Lo logrado hoy:
   - 40 leads calificados en el sector Fintech/Pagos.
   - 15 DMs redactados y listos para tu visto bueno.
   
2. ⚠️ Frenos o Errores detectados:
   - 2 prospectos tenían URLs inactivas; el Agente Intel los dejó en pausa para reintento manual.

3. 🚀 Siguiente paso recomendado:
   - Aprobar los 5 DMs de mayor score en 1-clic desde tu dashboard.
```
