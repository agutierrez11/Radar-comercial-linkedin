# Radar Comercial: Relationship Intelligence (BYOD MVP)

Este repositorio contiene las especificaciones, código base y desarrollo del MVP para **Radar Comercial**, una plataforma SaaS híbrida B2B/B2C que permite a los comerciales y empresas mapear, segmentar y utilizar relaciones de primer grado preexistentes (Warm Pipeline Mining) para acelerar las ventas.

---

## 🚀 Propuesta de Valor

- **Warm Pipeline Mining vs Cold Outreach:** 20x mejores tasas de respuesta conectando a través de relaciones ya establecidas en LinkedIn, en lugar de bases de datos de contactos fríos (Apollo/Lusha).
- **Bring Your Own Data (BYOD):** Carga segura y encriptada del ZIP de conexiones de LinkedIn sin ceder la propiedad de la red a la empresa (Wallet Privado).
- **Semáforo de Intros:** Los directores de ventas y el CRM corporativo solo ven si hay una conexión viva con una cuenta clave. El comercial mantiene el control absoluto y decide cuándo y a quién presentar a cambio de comisiones/bounties.
- **Enriquecimiento Semántico Inteligente:** Uso de Embeddings y Procesamiento de Lenguaje Natural para emparejar perfiles (ej. CFO con responsabilidades de Tesorería) y enriquecimiento automático del perfil de la empresa mediante scraping.

---

## 🛠️ Arquitectura Técnica del MVP

1. **Extensión de Chrome (Manifest V3):**
   - Inyección de scripts seguros en LinkedIn.
   - Detección de cuentas objetivo del CRM (HubSpot/Salesforce) mientras el vendedor navega.
   - Widget integrado para sugerencia de pitcheos con normalización geográfica.
2. **Servicio Backend (FastAPI / Python):**
   - API de autenticación y carga de archivos ZIP de LinkedIn.
   - Procesamiento de embeddings de similitud semántica (cargos, industrias, productos).
   - Integración OAuth con CRM (HubSpot en la primera fase).
   - Encriptación simétrica AES-256 del lado del cliente para salvaguardar los contactos en el monedero.
3. **Frontend Dashboard (React / Vite):**
   - Panel interactivo con búsquedas en tiempo real, filtros geográficos inteligentes e integraciones de plantillas de copia directa (pitches warm).

---

## 📅 Roadmap de Ejecución (6 - 8 Meses)

- [ ] **Fase 1: MVP Web Privado (Silo B2C) - Mes 1 y 2 (8 semanas):**
  - Carga local de ZIP y renderización de grafo interactivo 3D.
  - Procesador de texto para normalización de países/acentos.
- [ ] **Fase 2: Extensión de Chrome & HubSpot - Mes 3 y 4 (8 semanas):**
  - Desarrollo del plugin de HubSpot y extensión de Chrome básica para alertar sobre cuentas objetivo.
- [ ] **Fase 3: Cifrado Enterprise & Salesforce - Mes 5 al 8 (16 semanas):**
  - Cifrado Zero-Knowledge e ingreso al AppExchange de Salesforce (aprobación de Security Review).
