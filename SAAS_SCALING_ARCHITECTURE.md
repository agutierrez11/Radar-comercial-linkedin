# Arquitectura de Escalamiento SaaS: Radar Comercial + NERV OS

Este documento detalla la hoja de ruta técnica y de infraestructura para transformar el prototipo local actual en una plataforma SaaS/DaaS multiusuario, escalable y de alta disponibilidad para el mercado global.

---

```
                               ┌────────────────────────────────┐
                               │       Radar Comercial UI       │
                               │  (Vercel CDN / SPA Client-Side)│
                               └───────────────┬────────────────┘
                                               │
                                               │ (WebSockets / SSE)
                                               ▼
                               ┌────────────────────────────────┐
                               │          FastAPI Gate          │
                               │     (Google Cloud Run / API)   │
                               └───────────────┬────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
       ┌───────────────────────────────┐               ┌───────────────────────────────┐
       │     Celery Task Workers       │               │       Supabase Cloud DB       │
       │     (Swarm Agent Engine)      │               │   (Global Cache & Accounts)   │
       └───────────────┬───────────────┘               └───────────────▲───────────────┘
                       │                                               │
                       └───────────────────────────────────────────────┘
```

---

## Los 4 Pilares de la Arquitectura SaaS

Para lograr que el sistema soporte miles de usuarios simultáneos reduciendo a la vez los costos de infraestructura al mínimo, el camino de ingeniería se divide en los siguientes pilares:

### 1. Desacoplamiento de Capas (API-First & Client-Side Privacy)
Actualmente, el front-end corre como un HTML estático local y el back-end de agentes está empotrado en la interfaz de Streamlit. Para escalar a producción:
*   **Front-end (Radar Comercial):** Migración a una Single Page Application (SPA) moderna con **React + Vite / Next.js**, alojada en un CDN global de baja latencia como **Vercel** o Netlify. 
    *   *Privacidad en el cliente:* El parsing del archivo ZIP y CSV de LinkedIn se mantiene 100% del lado del cliente (Client-Side). El servidor central nunca recibe ni almacena los miles de contactos de tus usuarios, reduciendo los costos de almacenamiento a cero y garantizando el cumplimiento de normativas de privacidad (GDPR/LFPDPPP).
*   **Back-end (NERV OS Engine):** El motor de agentes (definido en `crew_engine.py`) se expone como una API REST mediante **FastAPI**.
    *   Se despliega en contenedores auto-escalables con **Google Cloud Run** o AWS ECS, configurados con escalamiento a cero (`min_instances = 0`) para no generar costos cuando no hay actividad de prospección.

### 2. Base de Datos Centralizada y Efecto Red de Datos (Data Flywheel)
Sustitución del archivo local SQLite (`nerv_cache.db`) por una base de datos relacional administrada en la nube como **Supabase (PostgreSQL)**.
*   **La Caché Global:** Cuando un vendedor analiza a un prospecto (ej. *Nu México*), el Swarm de NERV ejecuta la investigación web profunda (OSINT), extrae los dolores del negocio y los guarda en la base de datos centralizada.
*   **Costo Incremental Cero:** Si un segundo vendedor en cualquier parte del mundo intenta analizar a *Nu México*, el sistema no gasta créditos en las APIs de LLM o de Google Search (Serper). Le devuelve el dossier estructurado de la caché centralizada en milisegundos.
*   **Valor Defendible:** A mayor cantidad de usuarios, la base de datos de empresas enriquecidas de LATAM se vuelve más completa, haciendo que el producto sea más rápido, barato y valioso de forma automática.

### 3. Procesamiento Asíncrono y WebSockets (Mensajería en Vivo)
La ejecución completa del enjambre de agentes (auditoría, reflexión y simulación del comité de compras) toma entre 1.5 y 3 minutos, lo que causaría un timeout en conexiones HTTP síncronas estándar.
*   **Cola de Mensajería:** Las solicitudes de análisis comercial se envían a una cola de tareas distribuida gestionada con **Celery + Redis** (o Google Cloud Tasks).
*   **Transmisión de Estado (WebSockets / SSE):** El cliente mantiene una conexión WebSockets abierta. A medida que los agentes trabajan en la cola, el servidor transmite su estado de forma interactiva (ej. `[Investigador] buscando noticias en Google...`, `[Auditor] detectando alucinaciones...`) para pintar barras de progreso dinámicas en la interfaz del usuario.

### 4. Autenticación, Monetización e Integraciones (Stripe / CRM)
*   **Autenticación de Usuarios:** Integración de **Clerk** o Auth0 para el inicio de sesión y gestión de accesos corporativos.
*   **Monetización basada en Créditos (Stripe):**
    *   *Plan Básico ($10 USD/mes):* Acceso al tablero de Radar Comercial + 15 análisis inteligentes NERV al mes.
    *   *Plan Pro ($30 USD/mes):* Acceso al tablero + 100 análisis inteligentes NERV al mes.
*   **Integración con CRMs:** Conexión nativa con HubSpot, Salesforce o Pipedrive para que con un solo clic en la interfaz, el dossier estratégico generado por NERV se adjunte automáticamente como nota en el lead del CRM del vendedor.
