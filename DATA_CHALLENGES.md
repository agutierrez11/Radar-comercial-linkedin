# Retos de Ingeniería y Calidad de Datos (Data Challenges)

Este documento detalla los problemas reales de calidad, estructura y completitud de datos identificados al procesar las exportaciones oficiales de LinkedIn (`Connections.csv`), y cómo deben ser resueltos a nivel de código en el MVP.

---

## 1. El Desafío Geográfico (Falta de País)
*   **El Problema:** La exportación nativa de LinkedIn (`Connections.csv`) **no incluye el país ni la ubicación** del contacto. Solo provee: `First Name`, `Last Name`, `URL`, `Email Address`, `Company`, `Position`, `Connected On`.
*   **Por qué es crítico:** Para empresas como Netpay, que solo operan en México, o PayCash, que expande por países específicos, un comercial no puede trabajar con leads internacionales mezclados.
*   **La Solución (Motor de Inferencia Geográfica):**
    1.  **Sufijos de Correo:** Analizar el TLD de los correos corporativos (ej. `.mx` -> México, `.cl` -> Chile, `.co` -> Colombia, `.pe` -> Perú).
    2.  **Mapeo de Entidades y Sedes:** Crear un catálogo de empresas conocidas y sus países operativos (ej. *"Clip"* o *"Innovasport"* -> México).
    3.  **Normalización Diacrítica (El caso "Cancún"):** El script de análisis inicial fallaba con nombres de empresas locales con acentos (ej. *"HumanTalent Cancún"* quedaba como Desconocido porque el filtro buscaba la cadena estricta `cancun`). Se implementó una normalización unicode para remover acentos antes de procesar (`Cancún` -> `cancun`).

---

## 2. El Desafío de la Caducidad (Datos Estáticos vs. Tiempo Real)
*   **El Problema:** El CSV es una foto estática en el tiempo. Si un contacto cambia de empleo o es promovido mañana, la base de datos local queda obsoleta de inmediato.
*   **El Reto Técnico:** El CSV no discrimina si la empresa listada es la actual o la anterior a menos que entres al perfil en vivo en LinkedIn.
*   **La Solución de Actualización Híbrida:**
    1.  **Barrido Lento (Client-Side):** Para evitar bloqueos por parte de los sistemas de detección de scrapers de LinkedIn, la extensión de Chrome debe visitar de forma aleatoria e incremental un máximo de **15 a 20 perfiles al día** en segundo plano mientras el comercial navega.
    2.  **Enriquecimiento On-Demand (API Server):** Para leads prioritarios en cuentas objetivo (deals activos en HubSpot), el servidor consulta de forma programática APIs de enriquecimiento (ej. *Proxycurl* o *People Data Labs*) para actualizar el puesto de inmediato.
    3.  **Disclaimer UI:** Es obligatorio incluir un disclaimer en la interfaz del comercial advirtiendo que los datos estáticos tienen un margen de desactualización natural y se recomienda verificar a mano antes del envío.

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
