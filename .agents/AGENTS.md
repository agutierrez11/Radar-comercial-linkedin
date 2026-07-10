# Reglas del Agente para Radar Comercial (BYOD Relationship Intelligence)

Este archivo define las reglas persistentes, contexto de negocio y arquitectura técnica del proyecto **Radar Comercial**. Cualquier agente de Antigravity que trabaje en esta bóveda/proyecto DEBE leer e interiorizar este contexto al iniciar cada sesión.

---

## 📌 Contexto de Negocio e Idea Core

1. **Producto:** **Radar Comercial** (antes *linkedin-b2b-radar* o *boveda-sales-navigator*).
2. **Propósito:** Minería inteligente de relaciones de primer grado en LinkedIn para acelerar la velocidad de venta (Warm Pipeline Mining).
3. **El Modelo BYOD (Bring Your Own Data):** El usuario exporta su ZIP de LinkedIn y lo sube al sistema.
4. **Política de Privacidad y Conflicto del Vendedor:** 
   - La red de contactos es del comercial (su patrimonio).
   - Los datos se procesan en un contenedor privado/silo encriptado del lado del cliente (Zero-Knowledge). La empresa **no puede ver** ni poseer la red del vendedor.
   - En el CRM de la empresa, solo se muestra un indicador de semáforo: *"Santi tiene un contacto cálido con esta cuenta"*. Para usarlo, se solicita una introducción que el vendedor aprueba individualmente.
5. **Esquema de Incentivos (Bounty Referral):** Oportunidades de co-selling interno donde la empresa paga un *bounty* ($150 USD) y comisión (2%) al comercial que done su puente cálido para cerrar una cuenta objetivo.
6. **Valor Agregado (Enriquecimiento y Similitud Semántica):**
   - No buscamos "datos por kilo" (tipo Apollo/Lusha fríos). Buscamos similitud semántica de roles, cargos, productos y servicios mediante Embeddings e IA.
   - Enriquecimiento incremental de metadata mediante scraping de la web del cliente o APIs externas (Proxycurl/Apollo) para actualizar puestos, evitando bloqueos de LinkedIn.

---

## 🛠️ Reglas del Proyecto y Preferencias del Usuario (Antonio)

- **Alineación Comercial:** Cada decisión técnica o de diseño en el dashboard, extensión de Chrome o backend debe priorizar la facilidad de prospección del comercial individual y la velocidad de venta (Speed to Sell).
- **Tratamiento de Datos Rotos:** Indicar siempre un *disclaimer* en el dashboard y las notas de Obsidian, ya que la información de LinkedIn puede estar obsoleta o desestructurada (ej. países desconocidos, cargos históricos mezclados).
- **Normalización de Texto:** Para la clasificación por países y cargos, siempre normalizar acentos y diacríticos (ej. Cancún -> cancun) para evitar falsos negativos en los filtros.
- **CI/CD Obligatorio:** Todo desarrollo debe tener en cuenta el pipeline de Integración y Despliegue Continuo (CI/CD). El código en `main` debe ser siempre desplegable, incluir pruebas automatizadas/linters y configuraciones para despliegue automatizado en la nube (GitHub Actions, Render, Vercel).
- **Tone & Language:** Comunicarse con el usuario de manera proactiva, en español, de forma directa, ágil y con un tono técnico/de negocio de alto nivel.

---

## 📁 Estructura del Workspace Recomendada

- `/extension/` - Extensión de Google Chrome (Manifest V3) para extracción/interacción.
- `/backend/` - API REST en FastAPI/Node.js para procesamiento de ZIP, matching semántico y conexión OAuth con CRMs.
- `/frontend/` - Interfaz web interactiva del Dashboard en React/Vite.
- `README.md` - Resumen del proyecto, arquitectura y comandos de inicio.
