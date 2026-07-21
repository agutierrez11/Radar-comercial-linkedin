# Retos de Ingeniería y Calidad de Datos (Data Challenges)

Este documento detalla los problemas reales de calidad, estructura y completitud de datos identificados al procesar las exportaciones oficiales de LinkedIn (`Connections.csv`), y cómo deben ser resueltos a nivel de código en el MVP.

---

## 1. El Desafío Geográfico (Falta de País)
*   **El Problema:** La exportación nativa de LinkedIn (`Connections.csv`) **no incluye el país ni la ubicación** del contacto. Solo provee: `First Name`, `Last Name`, `URL`, `Email Address`, `Company`, `Position`, `Connected On`.
*   **Por qué es crítico:** Para empresas como Netpay, que solo operan en México, o PayCash, que expande por países específicos, un comercial no puede trabajar con leads internacionales mezclados.
*   **La Solución (Normalización LLM en Lote):**
    *   No usar diccionarios de reglas ni sufijos de correo (se rompen con cada variante y glitch como el cirílico).
    *   **Proceso:** Extraer todos los strings únicos que denotan ubicación (ya sea inferidos del nombre de la empresa, de la posición, o de exportaciones complementarias) y enviarlos en lote (batch) a un modelo rápido y económico como **Claude Haiku**. 
    *   Se le pide al LLM devolver País y Ciudad normalizados en JSON estructurado. A $1/$5 por millón de tokens, normalizar miles de ubicaciones cuesta centavos.

---

## 2. El Desafío de la Caducidad (Datos Estáticos vs. Tiempo Real)
*   **El Problema:** El CSV es una foto estática en el tiempo. Si un contacto cambia de empleo o es promovido mañana, la base de datos local queda obsoleta de inmediato.
*   **El Reto Técnico:** El CSV no discrimina si la empresa listada es la actual o la anterior, ni muestra fecha de inicio (a diferencia de Positions.csv propio). No hay historial, solo una "foto fija".
*   **La Solución (Snapshots Periódicos y Diff):**
    *   **NO usar scraping en vivo** (viola los Términos de Servicio de LinkedIn, riesgo alto de suspensión de cuenta).
    *   **El Motor de Diff:** Diseñar el sistema basado en exportaciones periódicas. El usuario exporta su `Connections.csv` cada mes. El sistema guarda cada versión y compara (hace un *diff*).
    *   Si el campo `Company` de un contacto cambia entre el mes N y el N+1, se levanta una alerta de "Job Change". No es tiempo real, pero es **100% honesto, legal y sostenible**.
    *   *Proxy débil alternativo:* Usar `Connected On` para inferir relación dormida vs. reciente, pero no para antigüedad en el puesto.

---

## 3. El Desafío de los Campos Vacíos (Emails Ocultos)
*   **El Problema:** Por políticas de privacidad de LinkedIn, si un contacto tiene desactivada la opción *"Permitir que mis contactos descarguen mi correo"*, la columna de `Email Address` en el CSV exportado **viene completamente vacía**. En exportaciones promedio, más del **70% de los correos están en blanco**.
*   **La Solución de Enriquecimiento:**
    1.  Cruzar el dominio de la empresa con el formato estándar de correos corporativos (ej. `{nombre}.{apellido}@{empresa}.com`).
    2.  Utilizar endpoints de búsqueda de correos de APIs de enriquecimiento comercial cuando el comercial decida iniciar la campaña.

---

## 4. El Desafío de Limpieza de Texto (Text Noise)
*   **El Problema:** Los usuarios en LinkedIn suelen agregar emojis, pronombres o certificaciones en sus campos de nombre (ej. *"Sara Nuñez Pernasetti 🇲🇽"*, o *"Juan Perez (PMP®)"*).
*   **La Solución:** Implementar regex de limpieza de nombres en el pipeline de ingesta para separar nombres limpios de títulos, emojis y pronombres para que la generación de copys personalizados sea natural (evitando correos que digan: *"Hola Sara Nuñez Pernasetti 🇲🇽, vi que..."*).

---

## 5. El Desafío de las Métricas de Mensajería (ZIP On-Demand)
*   **El Problema:** El historial de mensajes (`messages.csv`) solo está disponible cuando el usuario solicita manualmente la exportación de datos a LinkedIn (proceso que tarda horas). Intentar medir "actividad en los últimos 30 días desde HOY" usando un ZIP descargado hace semanas genera métricas vacías u obsoletas, y exigir una descarga diaria de ZIP a LinkedIn es inviable en términos de UX.
*   **La Solución (Analítica Híbrida de Cohorte + CRM Incremental Local):**
    1.  **Analítica de Cohorte del ZIP (Snapshot Analytics):** Al procesar un `messages.csv`, las métricas de respuesta (Reply Rate, días promedio de respuesta) se calculan relativas a la **fecha máxima registrada en el propio archivo**, no al tiempo presente real (`new Date()`). Se presenta al usuario como *"Salud de Respuesta en la Muestra Exportada"*.
    2.  **Tracking Incremental Local (Dashboard / Chrome Extension):** La actividad en tiempo real de los últimos 30 días se actualiza **localmente** cada vez que el vendedor ejecuta una acción en Radar Comercial (marcar estado de pipeline, enviar pitch con la extensión o agendar reunión), guardando el evento en la BD/localStorage local sin depender de LinkedIn.

