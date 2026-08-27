---
name: b2b-ai-sdr-agency
description: Orquestación de una Agencia de Ventas Autónomas y Enjambre SDR (CrewAI + BrightData AI-SDR + CompAI) para prospección B2B, filtrado estricto por ICP, enriquecimiento de cuentas objetivo y generación de secuencias outbound multicanal.
---

# B2B AI SDR Agency Skill — Enjambre Agéntico de Ventas B2B

Esta habilidad transforma la célula agéntica en una **Agencia de Ventas Autónomas**, desplegando roles especializados para prospección, investigación de cuentas, puntuación contra ICP (Ideal Customer Profile) y generación de secuencias outbound de alta conversión.

---

## 🛠️ Arquitectura del Enjambre Agéntico de Ventas (SDR Swarm)

```
 [ Definición ICP ] ──► [ 1. Account Discovery Agent ] ──► [ 2. ICP Qualifier Agent ]
                                                                     │
 [ CRM Sync ] ◄── [ 4. Campaign & Outreach Agent ] ◄── [ 3. Trigger Analyst Agent ]
```

### Roles del Enjambre

1. **Account Discovery Agent (Hunter):**
   - Utiliza scraping ético y motores como `Crawl4AI` o `Serper` para descubrir empresas objetivo dentro del segmento seleccionado (ej. Fintech, E-commerce, PayTech en México/LATAM).
   - Extrae ejecutivos clave (C-Level, VPs de Pagos, Directores de Producto/Operaciones).

2. **ICP Qualifier Agent (Scorer):**
   - Valida el encaje del prospecto contra la matriz ICP bajo criterios estrictos:
     - Tamaño de empresa / TPV estimado procesado.
     - Stack tecnológico (procesadores de pago, ERPs, ecommerce platforms).
     - Geografía y mercado activo.
   - Asigna una puntuación `ICP_Match_Score` de 0 a 100 y descarta falsos positivos.

3. **Trigger Event Analyst (Hook Miner):**
   - Analiza eventos disparadores recientes:
     - Noticias de rondas de inversión o expansión geográfica.
     - Nuevas ofertas de trabajo (ej. contratando ingenieros de pagos o backend).
     - Cambios en políticas regulatorias o de adquirencia.
   - Extrae el "gancho" comercial exacto para romper el hielo.

4. **Outbound Campaign & Outreach Agent (Copywriter):**
   - Redacta secuencias multicanal hiper-personalizadas (Email frío + InMail de LinkedIn + WhatsApp B2B).
   - Aplica metodologías comerciales probadas (**MEDDIC**, **Challenger Sale**, **SPIN Selling**).
   - Genera variaciones A/B probadas en simulaciones contra gemelos digitales de buyer personas.

5. **CRM & Pipeline Synchronization Agent (RevOps Sync):**
   - Registra el lead cualificado en el CRM (HubSpot, Salesforce, CompAI CRM).
   - Asigna tareas de seguimiento y notifica al ejecutivo de cuenta (AE) por Telegram/Slack cuando un lead demuestra alta intención.

---

## 📋 Prompt Template para Ejecutar el Enjambre SDR

Cuando solicites a la célula ejecutar una prospección agéntica, utiliza la siguiente estructura:

```markdown
/teamwork-preview Ejecuta la Agencia de Ventas B2B para el ICP:
- Industria: [Ej. E-commerce / PayTech]
- Geografía: [Ej. México / Colombia / Peru]
- Puestos Objetivo: [Ej. VP of Payments, Chief Revenue Officer, CEO]
- Criterios ICP: [Ej. TPV > $500k USD/mes, usa Shopify/Magento, expansión regional]
- Tesis del Valor: [Ej. Reducción de comisiones de adquirencia y pasarelas vía API]
```

---

## 🔒 Reglas Inmutables de Prospección

1. **Zero Placeholder Policy:** Todos los correos y mensajes generados deben incluir variables reales investigadas del prospecto, jamás textos genéricos tipo `"Hola [Nombre]"` sin personalizar.
2. **Respeto a la Privacidad:** No enviar spam masivo sin cualificación. Priorizar calidad de encaje ICP sobre volumen.
3. **Métrica Norte:** Medir el éxito por **Sales Qualified Leads (SQLs)** agendados en pipeline, no por vanity metrics.
