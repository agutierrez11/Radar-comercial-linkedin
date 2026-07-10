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

---

## 3. El Flujo de Onboarding RLHF en 1 Clic (Confirmación de Entidades)

Para garantizar la precisión de los diccionarios de venta sin forzar al usuario a escribir nada, el proceso de Onboarding implementará un flujo de **Reinforcement Learning from Human Feedback (RLHF)** basado en micro-confirmaciones:

```
[ Lee Positions.csv ] ──► [ Búsqueda Auto: "Clip" -> clip.mx ] ──► [ Onboarding UI: "¿Es esta tu empresa? [Sí/No]" ]
```

1.  **Búsqueda Automática en Segundo Plano:** 
    *   Al subir el ZIP, el sistema lee `Positions.csv` y detecta las empresas (ej. *Clip*, *Fiserv*).
    *   El servidor busca automáticamente en internet (vía API de búsqueda) las URLs oficiales y resúmenes de negocio de esas marcas (ej. `https://www.clip.mx`).
2.  **La Micro-Tarjeta de Confirmación (RLHF):**
    *   En lugar de un formulario en blanco, el onboarding muestra una tarjeta interactiva muy limpia:
        > **"Confirmemos tu historial para activar tu Radar:"**
        > *   *¿Trabajaste en **Clip** y su web oficial es [clip.mx](https://www.clip.mx)?*  
        >     **[ Sí ]**  **[ No ]**
3.  **El Cierre del Círculo (Loop de Aprendizaje):**
    *   **Si el usuario hace clic en [ Sí ] (90% de los casos):** El sistema confirma la entidad, asocia el dominio, descarga la propuesta de valor y activa los diccionarios correctos. Todo con **un solo clic**.
    *   **Si hace clic en [ No ]:** El sistema le permite escribir rápidamente la URL correcta o buscar una alternativa, corrigiendo el modelo para futuros usuarios.

