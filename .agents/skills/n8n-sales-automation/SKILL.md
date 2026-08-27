---
name: n8n-sales-automation
description: Automatización de flujos de ventas multicanal con n8n (n8n-io/n8n). Orquestación 24/7 de pipelines de prospección, calificación con IA, enriquecimiento de leads y sincronización CRM.
---

# n8n Sales Automation Skill — Automatización Visual Multicanal

Esta habilidad define la arquitectura para crear flujos automatizados de ventas utilizando **n8n**, conectando servicios de IA (Gemini, OpenAI, Qwen) con APIs de prospección, correo electrónico, WhatsApp y CRMs.

---

## ⚡ Flujo Típico de Prospección 24/7

```
[ Webhook / Trigger ] ➔ [ Scraping Web / API ] ➔ [ Evaluación ICP con LLM ] ➔ [ Generación de Email ] ➔ [ Envio & Notificación Slack ]
```

### Componentes Clave
- **AI Agent Node:** Analiza los datos del lead y decide si asignar calificación *Hot Lead*.
- **Postgres / Supabase Node:** Almacena el historial de interacciones y evita duplicación de prospectos.
- **CRM Integration Node:** Crea o actualiza tratos en HubSpot / Salesforce de forma automática.
