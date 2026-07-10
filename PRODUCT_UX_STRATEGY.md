# UX de Cero Configuración: El Producto Invisible para Comerciales

Este documento define la estrategia de Experiencia de Usuario (UX) y arquitectura técnica para eliminar la fricción de curación de datos, asegurando la retención de los comerciales en el día a día.

---

## 1. La Ley del Menor Esfuerzo Comercial (El Problema)
Los comerciales B2B odian el trabajo administrativo. Odian llenar campos en el CRM, odian limpiar datos y odian configurar herramientas. 
*   Si la herramienta requiere que el comercial configure su línea de tiempo, escriba palabras clave, o cure falsos positivos (como separar el ethanol de Fiserv), **el comercial dejará de usar la plataforma a los 3 días.**
*   El éxito de **Radar Comercial** depende de que el valor se entregue de forma **invisible e instantánea**.

---

## 2. Los 3 Pilares del "Zero-Configuration Setup"

Para lograr un onboarding en 1 solo clic y sin fricción:

### Pilar A: Inferencia Automática de Industria (No preguntar palabras clave)
El usuario solo arrastra su ZIP. El sistema lee `Positions.csv` y hace lo siguiente de forma automática:
1.  **Detección de Compañía:** Identifica que trabajó en "Clip" y "Fiserv".
2.  **Enriquecimiento de Dominio:** Consulta una base de datos interna de industrias (o un micro-servicio) y cataloga:
    *   *Clip / Fiserv* -> Categoría: *Procesamiento de Pagos / Fintech*.
3.  **Carga Automática de Diccionarios:** El sistema asocia automáticamente el diccionario de palabras clave de pagos (`terminal`, `cobro`, `pagos`, `tasa`, `adquirente`) sin que el usuario tenga que escribir una sola palabra.

### Pilar B: Clasificación Inteligente en Segundo Plano (El Filtro Invisible)
Los algoritmos de filtrado (como la exclusión de reclutamiento, venta hacia mí o networking de ayuda) ocurren en el backend. 
*   El comercial **nunca ve la base de datos cruda** ni tiene que corregir las categorías.
*   En lugar de mostrarle una tabla con 1,700 chats clasificados, la interfaz solo le presenta las **acciones ejecutables de alto valor**:
    *   *"Tus 3 abridores históricos más efectivos para agendar citas."*
    *   *"3 prospectos tibios de tu época en Clip que acaban de cambiar de empleo."*

### Pilar C: Retroalimentación Implícita (Feedback en 1 Clic)
Si por algún error de algoritmo aparece un contacto irrelevante (como el caso de Alex con el etanol):
*   El comercial no entra a un panel de configuración a borrarlo.
*   Simplemente hace clic en **"Omitir"** o **"No es relevante"** en la tarjeta de sugerencia.
*   El sistema registra ese clic y ajusta la recomendación del modelo para ese usuario de forma silenciosa en segundo plano.
