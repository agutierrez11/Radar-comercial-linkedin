---
name: open-seo
description: Suite SEO Open-Source nativa con servidor MCP (Model Context Protocol) para auditar backlinks, ranking de competidores y palabras clave B2B mediante modelo BYOK (DataForSEO API) sin pagar suscripciones.
version: 1.0.0
---

# 🔍 OpenSEO (Servidor MCP y Analítica SEO BYOK)

Este skill proporciona la guía de integración de **OpenSEO** (`every-app/open-seo`) para auditar la presencia digital de competidores (Orsan, FEMSA, NetPay, Kioskos) y alimentar los agentes de investigación en **Paymind Growth Engine** y **Radar Comercial**.

---

## 🎯 1. Principios de Operación

1. **Modelo BYOK (Bring Your Own Key):** Conecta la API Key de **DataForSEO** para pagar centavos por consulta sin pagar licencias fijas de \$200 USD/mes en Semrush/Ahrefs.
2. **Servidor MCP Integrado:** Conecta directamente con agentes de IA (Antigravity/Claude Code) para realizar búsquedas de palabras clave en lenguaje natural.

---

## 🛠️ 2. Configuración del Servidor MCP en `mcp_config.json`

```json
{
  "mcpServers": {
    "open-seo": {
      "command": "npx",
      "args": ["-y", "@every-app/open-seo-mcp"],
      "env": {
        "DATAFORSEO_LOGIN": "tu_usuario_dataforseo",
        "DATAFORSEO_PASSWORD": "tu_password_dataforseo"
      }
    }
  }
}
```

---

## 📊 3. Casos de Uso Ejecutables

* **Investigación de Competidores B2B:**  
  *"Auditar el perfil de backlinks y palabras clave del dominio netpay.com.mx para detectar dolores de clientes."*
* **Rastreo de Posicionamiento:**  
  *"Evaluar el volumen de búsqueda mensual de la palabra clave 'Anexo 30 SAT gasolineras' en México."*
* **Enriquecimiento de Fichas de Leads:**  
  *"Consultar la autoridad de dominio de las empresas de los 344 leads ICP en Radar Comercial."*
