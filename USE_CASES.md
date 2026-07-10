# Casos de Uso del Producto (Product Use Cases)

Este documento detalla las tres configuraciones de adopción comercial y flujos de usuario para **Radar Comercial**, definiendo el valor de negocio, la interacción con el CRM y la lógica de asignación para cada escenario.

---

## 👤 Caso 1: Bottom-Up (Solo el Vendedor usa la herramienta)
*El comercial adopta la herramienta de manera individual como su "arma secreta" de prospección.*

### Flujo de Usuario:
1.  **Carga y Segmentación:** El vendedor descarga su ZIP de LinkedIn, lo sube a su dashboard privado de Radar y la IA clasifica su red geográficamente (infiriendo el país) y por nivel de decisión (C-Level, Directores).
2.  **Identificación de Oportunidades:** El vendedor introduce el ICP de su producto actual (ej. Toku o Netpay). La IA resalta los contactos con mayor probabilidad de cierre (Warm Leads).
3.  **Prospección y Contacto:** El vendedor utiliza las plantillas de pitcheo sugeridas por la IA para contactar al lead vía LinkedIn o correo personal.
4.  **Carga Selectiva al CRM:** Cuando la conversación avanza y se convierte en un **deal caliente** (ej. el cliente solicita cotización o agenda una demo), el vendedor **registra manualmente el deal y el contacto en el CRM de la empresa** para asegurar su comisión.

### Valor de Negocio:
*   **Vendedor:** Maximiza su tasa de cumplimiento de cuota usando atajos de confianza.
*   **Empresa:** Recibe leads pre-calificados y de alta probabilidad en su CRM sin pagar licencias de software adicionales.
*   **Fricción:** Mínima. No requiere aprobación de TI ni integración corporativa.

---

## 🏢 Caso 2: Top-Down (Solo la Empresa usa la herramienta)
*La empresa adquiere el software para su CRM (HubSpot/Salesforce), pero los vendedores no instalan la extensión ni comparten sus redes personales.*

### Flujo de Usuario:
1.  **Enriquecimiento Forense:** La herramienta escanea la base de datos de leads fríos de la empresa y la enriquece escrapeando las webs de las compañías objetivo (lógica de José: tecnologías utilizadas, verticales específicas, tamaño).
2.  **Detección de "Leads Calientes":** La IA clasifica y prioriza los leads que tienen la mayor probabilidad de compra.
3.  **Asignación Inteligente (El Algoritmo de Match):** Dado que no tenemos acceso a las redes de 1er grado de los vendedores, la herramienta asigna el lead al comercial óptimo usando tres criterios:
    *   **Encaje de Vertical/Geografía (ICP Match):** Asignar al vendedor especializado en ese sector o región (ej. Netpay asigna leads de eCommerce en México a comerciales de México).
    *   **Historial de Éxito (Performance Match):** Asignar al comercial con mayor tasa de cierre (*Closed-Won*) en cuentas con perfiles similares.
    *   **Proximidad de Red Indirecta (2nd Degree Match):** El sistema escanea la red corporativa de la empresa (los contactos institucionales del CRM) para identificar si algún miembro del equipo de ventas tiene conexiones de segundo grado en común.

### Valor de Negocio:
*   **Empresa:** Automatiza la prospección fría y asegura que los leads más valiosos sean atendidos por el vendedor con mayor probabilidad de éxito.
*   **Vendedor:** Recibe leads altamente calificados directamente en su bandeja del CRM sin esfuerzo de prospección.
*   **Fricción:** Media. Requiere integración a nivel administrador de CRM y presupuesto corporativo.

---

## 🤝 Caso 3: Híbrido (Empresa y Vendedor usan la herramienta)
*El modelo ideal de colaboración. Ambos mundos se superponen bajo una arquitectura segura.*

### Flujo de Usuario:
1.  **Alineación de Objetivos:** La empresa sube su lista de "Cuentas Objetivo" (Target Accounts) a HubSpot.
2.  **Carga del Monedero Privado:** Los vendedores suben sus ZIPs a sus contenedores encriptados locales (Client-Side).
3.  **Cruce de Datos Seguro (Semáforo):** El backend compara los hashes anonimizados. Si el *Vendedor A* está conectado con el CFO de una Cuenta Objetivo:
    *   El CRM de la empresa muestra una alerta: *"Puente cálido disponible"*.
    *   El *Vendedor A* recibe una alerta en su extensión: *"Tu empresa quiere cerrar esta cuenta y tú tienes el contacto directo. Facilita la intro."*
4.  **Activación de Bounty:** Si el vendedor decide hacer la introducción y se concreta la venta, el sistema gestiona de forma automática el pago del **Bounty interno de co-selling** ($150 USD + 2% de comisión) al vendedor que facilitó el contacto.

### Valor de Negocio:
*   **Empresa:** Desbloquea la red de contactos acumulada de todo su equipo de ventas de forma legal y ética.
*   **Vendedor:** Monetiza su red de contactos personal de forma segura sin perder su propiedad.
*   **Fricción:** Alta inicial. Requiere adopción del equipo y configuración de políticas de privacidad claras.
