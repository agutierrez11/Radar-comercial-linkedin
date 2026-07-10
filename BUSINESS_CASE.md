# Case de Negocio y Posicionamiento Competitivo: Radar Comercial

Este documento recopila las bases de posicionamiento, diferenciación competitiva y estrategia de validación de mercado para **Radar Comercial**. Está diseñado como material de alineación estratégica para el equipo de ingeniería y ciencia de datos.

---

## 1. El Problema de Mercado (Las Tres Fricciones)

1.  **La muerte de la prospección en frío (Outbound Decay):** Los filtros de spam de Google/Outlook y la saturación de mensajes genéricos han desplomado las tasas de conversión del correo frío a menos del 1%.
2.  **El "Cajón Vacío" de los CRMs:** Los vendedores odian rellenar el CRM a mano y, más aún, se niegan a subir sus redes de contactos personales de LinkedIn por temor a perder su patrimonio profesional si cambian de empresa.
3.  **Datos "por kilo" obsoletos:** Plataformas como Apollo o Lusha venden bases de datos masivas pero frías. No discriminan si hay una relación de confianza previa ni analizan semánticamente el encaje de perfiles y empresas en LATAM.

---

## 2. La Solución: Radar Comercial (BYOD + Private Wallet)

Un motor de inteligencia relacional que permite minar las conexiones existentes de los vendedores de forma segura, respetando la propiedad individual de la red y conectándose de manera transparente al CRM corporativo.

*   **Bring Your Own Data (BYOD):** Carga descentralizada del ZIP de LinkedIn por parte del vendedor.
*   **Arquitectura Zero-Knowledge (Monedero Privado):** La empresa no posee ni puede exportar la red del vendedor. El CRM solo recibe una alerta de coincidencia (semáforo). El comercial decide cuándo facilitar la introducción para un negocio activo.
*   **Co-Selling Incentivado (Internal Bounties):** Un esquema gamificado donde la empresa premia al comercial que comparte un puente cálido interno para acelerar un trato en el pipeline de un compañero.

---

## 3. Matriz Comparativa (¿Por qué nosotros?)

| Criterio | Apollo / Lusha | Clay / Folk | LeadDelta | **Radar Comercial** |
| :--- | :--- | :--- | :--- | :--- |
| **Enfoque Principal** | Datos fríos masivos (Email/Teléfono) | CRM alternativo / Enriquecimiento de datos | Gestión personal de inbox en LinkedIn | **Minería relacional e intros cálidas en equipo** |
| **Modelo de Privacidad** | Datos públicos/comprados sin consentimiento | Datos centralizados en base de datos propia | Datos en la nube del usuario individual | **Zero-Knowledge (Monedero Privado encriptado)** |
| **Integración con CRM** | Exportación de contactos (push plano) | Compite directamente (quieren reemplazar el CRM) | Sincronización básica unidireccional | **Plugin nativo de acompañamiento (semáforo de intros)** |
| **Fricción de Entrada** | Baja (Pagar suscripción) | Alta (Requiere migración o setup complejo) | Baja-Media (Extensión individual) | **Baja (Se monta sobre el CRM existente en 1 clic)** |
| **Mercado Target** | Equipos de marketing y SDRs fríos | Startups y Operations Managers | Profesionales y Freelancers individuales | **Equipos de venta B2B y Hunters Corporativos** |

---

## 4. ¿Por qué nos promoverán los Marketplaces de CRM (HubSpot/Pipedrive)?

Los CRMs líderes no nos ven como competencia, sino como un **acelerador de adopción**:
*   Aumentamos el uso del CRM porque el vendedor tiene un incentivo directo (comisiones/bounties de introducción) para mantener la herramienta abierta y conectar sus datos.
*   Incrementamos la **velocidad de venta (Sales Velocity)** al acortar la fase de prospección de semanas a minutos gracias al mapeo de puentes cálidos.

---

## 5. Estrategia de Validación de Riesgo Mínimo (MVP Concierge)

Para validar la disposición de pago antes de invertir recursos de desarrollo en la extensión de Chrome y el backend, ejecutaremos una prueba piloto de una semana:

```
[ Vendedor comparte Connections.csv ] ──► [ Procesamiento Manual local con IA ] ──► [ Dashboard HTML interactivo personalizado ]
                                                                                                    │
                                                                                                    ▼
                                                                                         [ Validación de Pago ($10 USD) ]
```

1.  **Captura de Leads:** Solicitar el CSV de LinkedIn a un grupo de 15 comerciales objetivo a cambio de un análisis relacional gratuito.
2.  **Procesamiento:** Correr nuestro script de Python para clasificar e inferir países, normalizando acentos (ej. Cancún -> cancun).
3.  **Entrega del Dashboard:** Entregar el HTML interactivo personalizado con las sugerencias de pitcheo dinámicas por ICP (Toku/Netpay).
4.  **Validación de Monetización:** Ofrecer la actualización mensual automática por una tarifa piloto de **$10 USD/mes**. Si el 20-30% acepta pagar por el entregable manual, procedemos a automatizar la ingeniería de software.
