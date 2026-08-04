# Análisis de Verticales con Teoría de Grafos (Starpago)

El objetivo es modelar las verticales comerciales de Starpago no como silos aislados, sino como un **Grafo Conectado** donde los *nodos* son las industrias y las *aristas (edges)* son las infraestructuras de pago compartidas. Utilizando conceptos de algoritmos de optimización (como Dijkstra para "el camino de menor fricción a la monetización"), revelaremos cómo cruzar (cross-sell) clientes de una vertical a otra.

## Open Questions
> [!WARNING]
> ¿Deseas que este análisis de grafos reemplace alguna sección actual del Dossier, o prefieres que vivan en un nuevo documento dedicado exclusivamente a la Arquitectura de Verticales (ej. `estrategia_grafos_starpago.md`) para presentarlo como un anexo visual en tu entrevista?

## Proposed Changes

### 1. Definición del Modelo de Grafo
Modelaremos el ecosistema de la siguiente manera:
*   **Nodos (Verticales de Negocio):**
    1. iGaming (Casinos / Apuestas)
    2. E-Sports & Gaming (Ligas, Publishers)
    3. Crypto & Forex (Exchanges, Brokers)
    4. E-commerce Cross-Border (Retailers Internacionales, Plataformas SaaS)
*   **Aristas (El 'Pegamento' o Infraestructura Compartida):**
    *   *Edge A:* Payouts transfronterizos (Liquidación FX).
    *   *Edge B:* APMs Locales (OXXO, SPEI, Pix, PSE).
    *   *Edge C:* Motor Anti-Fraude / Liability Shift.
    *   *Edge D:* Cumplimiento Regulatorio y KYC.
*   **El "Shortest Path" (Dijkstra):** El camino más corto para maximizar el LTV (Life Time Value) de la infraestructura de Starpago es venderle *todas* las aristas a un nodo, y usar ese caso de éxito para saltar al nodo adyacente que comparte la misma arista.

### 2. Creación del Artefacto de Grafos (Mermaid Diagram)
Crearé un diagrama usando `mermaid.js` que el usuario puede visualizar y exportar. El diagrama mostrará visualmente cómo:
- Un jugador deposita en Crypto.
- El Exchange usa la infraestructura de FX (Arista A).
- El usuario lo gasta en iGaming (Nodo 1).
- El Casino hace Payout a un Streamer de E-sports (Nodo 2).

### 3. Argumentario "Cross-Selling" (Teoría de Juegos)
Definiremos los incentivos (Game Theory) de por qué un merchant de E-commerce Crossborder debería adoptar soluciones de iGaming (ej. gamificación de pagos, payouts instantáneos a proveedores locales). 

## Verification Plan

### Manual Verification
- Validar que el diagrama Mermaid se renderice correctamente en la interfaz.
- Asegurar que el pitch de venta (el "cruce" entre verticales) suene comercialmente agresivo y técnicamente viable para la entrevista.
