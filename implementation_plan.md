# Radar Comercial — Plan de Ejecución del Producto Core

**Propósito:** Minería inteligente de relaciones de primer grado en LinkedIn (Warm Pipeline Mining), depuración de red BYOD y enriquecimiento en vivo BYOK para acelerar la velocidad de venta (Speed to Sell).

---

## 🎯 Enfoque Actual del Sistema

1. **Depuración & Baselines del Vault:**
   - Mantenimiento estricto del baseline de **2,953 contactos limpios** de Antonio.
   - Algoritmo de scoring ICP para **296 contactos Clase A** (Alta Densidad de Monetización).
   - Persistencia inmutable en IndexedDB/localStorage (`crmState` + `contacts`).

2. **Enriquecimiento BYOK ("De Becario a CEO"):**
   - Integración con HarvestAPI / Apify para actualización en vivo de cargos, empresas y ubicaciones.
   - Integración con modelos de IA (Gemini 2.5 Flash, Qwen Disier, GPT-4o mini) mediante Bring Your Own Key (BYOK).

3. **Frontend & Resiliencia:**
   - Auto-sync ante cambios de conectividad (`online` listener).
   - Analítica RevOps y tablero de visualización A/B Vault.

---

## 📋 Próximos Pasos Ejecutables

1. **Despliegue CI/CD (`main`):** Git commit y push de las mejoras de estabilidad y reconexión automática en `index.html` / `staging.html`.
2. **Motor de Enriquecimiento BYOK:** Verificar pipeline de llamadas a HarvestAPI/Apify para perfiles con cargos desactualizados.
3. **Generador de DMs & Playbooks:** Prospección contextual de 1-clic usando las plantillas de Notion integradas en el Dashboard.
