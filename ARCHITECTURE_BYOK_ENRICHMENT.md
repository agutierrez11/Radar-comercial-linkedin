# 💎 Arquitectura BYOK (Bring Your Own Key) & Enriquecimiento Masivo

> **Documento de Arquitectura y Tesis Comercial de Radar Comercial**

---

## 1. 📌 La Tesis del Pipeline Histórico ("De Becario a CEO")

El archivo ZIP exportado de LinkedIn es un **snapshot estático con alta degradación temporal**:
- Cuando descargas tu red de LinkedIn, gran parte de los cargos y empresas corresponden al **momento exacto en que te conectaste** con esa persona (que puede ser hace 3, 5 o 10 años).
- En redes de profesionales senior (como las de 15k conexiones), **las personas que agregaste hace años como pasantes, analistas o coordinadores HOY en día son CEOs, VPs, Directores de Marketing o Fundadores**.
- Si un comercial solo prospecta con los datos planos del ZIP, está ciego ante el **70% de sus oportunidades enterprise**.

**Conclusión:** La prioridad técnica y comercial #1 es la **actualización de perfiles en vivo (Cargo Actual, Empresa Vigente, País/Ciudad Real y Último Post)**.

---

## 2. 🛡️ Modelo BYOK (Bring Your Own Key) y Regla de Cero Subsidio

1. **Antonio / La Plataforma paga $0 USD:** La plataforma provee el software, la normalización de datos, la clasificación de jerarquía y la interfaz de inteligencia comercial.
2. **El Cliente fondea su propio consumo:** El cliente crea sus cuentas en los proveedores de datos e IA, adquiere sus paquetes de créditos y pega sus API Keys en su navegador local (**Silo Zero-Knowledge en `localStorage`**).

---

## 3. 📊 Matriz de Proveedores y Estructura de Costos Reales

| Categoría | Proveedor Recomendado | Costo Estimado (Lote 15k Contactos) | Enlace de Referido / Afiliado |
| :--- | :--- | :--- | :--- |
| **Enriquecimiento LinkedIn** | **HarvestAPI** | ~$70 a $90 USD (por paquete de créditos) | `https://harvestapi.io/?ref=radarcomercial` |
| **Scraping Masivo por Lotes** | **Apify** | ~$49 a $60 USD (Plan Starter + proxies) | `https://apify.com?fpr=radarcomercial` |
| **Inteligencia Artificial (LLM)** | **OpenAI (GPT-4o mini)** | ~$3 a $5 USD (para >20k DMs) | `https://platform.openai.com` |
| **Inteligencia Artificial (LLM)** | **Google Gemini (2.5 Flash)** | $0.00 USD (Free Tier / Centavos) | `https://aistudio.google.com` |
| **Inteligencia Artificial (LLM)** | **Disier AI (Qwen 3.8-27B)** | ~$0.0008 USD / mensaje | `https://llm.disier.net` |

---

## 4. 💰 Programa de Afiliados y Monetización de Infraestructura

Todos los botones de "Obtener API Key" en el dashboard de Radar Comercial redirigen con parámetros de afiliado/referido (`?ref=radarcomercial` / `?fpr=radarcomercial`). De esta forma:
- El cliente obtiene tarifas directas de proveedor.
- Antonio recibe comisiones recurrentes o créditos de scraping por cada paquete que sus clientes contraten.
