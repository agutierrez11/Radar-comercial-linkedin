# Especificación del Piloto MVP (El Experimento de los 5 Amigos)

Este documento detalla el diseño técnico y operativo del primer experimento de validación sin servidor. El objetivo es permitir que un grupo de 5 amigos compartan de forma segura sus "contactos calientes" de LinkedIn para encontrar coincidencias e introducciones de valor de forma 100% local.

---

## 📅 El Flujo del Experimento (Paso a Paso)

```
[ Amigo 1 ] ──► Corre Script Local ──► Genera warm_contacts_amigo1.json
[ Amigo 2 ] ──► Corre Script Local ──► Genera warm_contacts_amigo2.json  ──► [ Antonio (Matcher) ] ──► Genera Dashboard Grupal (HTML)
[ Antonio ] ──► Corre Script Local ──► Genera warm_contacts_antonio.json
```

1.  **La Convocatoria:** Antonio pide a 5 amigos comerciales/fundadores de confianza que descarguen su ZIP de datos de LinkedIn.
2.  **El Procesamiento Local (Script 1):** Cada amigo corre un script de Python de forma local en su computadora. Este script analiza su ZIP, filtra únicamente a los contactos con los que **sí ha chateado** y genera un archivo ligero y limpio: `warm_contacts_[Nombre].json`.
3.  **El Envío:** Los amigos envían únicamente ese archivo `.json` a Antonio (sin compartir todo su ZIP completo ni sus conversaciones privadas).
4.  **La Consolidación (Script 2):** Antonio corre un script unificador en su computadora que lee los 5 archivos `.json` y genera un **Dashboard Interactivo en HTML** (`dashboard_alianza.html`) que revela las conexiones del grupo.

---

## 🛠️ Especificación de los Scripts

### Script 1: El Extractor Relacional (Local Scrubber)
*Este script lo ejecuta cada participante en su computadora.*

*   **Entrada:** Carpeta del ZIP de LinkedIn extraído (archivos `Connections.csv` y la carpeta de mensajes `messages/` o `Messages.csv`).
*   **Procesamiento:**
    1.  Lee el archivo de conexiones para obtener la lista base.
    2.  Analiza la bitácora de mensajes de la carpeta `messages/`. Cuenta el número de mensajes intercambiados con cada contacto.
    3.  **Filtro de Ruido (La regla de chateo):** Solo conserva los contactos con los que ha intercambiado **más de 2 mensajes**. Esto elimina los miles de contactos agregados por "ruido" que no recuerdan quién es el participante.
    4.  **Limpieza:** Remueve emojis y títulos sucios de los nombres.
*   **Salida:** Un archivo JSON (`warm_contacts_[nombre].json`) con la estructura:
    ```json
    [
      {
        "name": "Armando Herrera",
        "company": "Nu México",
        "position": "CEO",
        "email": "armando@nu.com.mx",
        "linkedin_url": "https://www.linkedin.com/in/...",
        "message_count": 14,
        "last_message_date": "2026-06-15"
      }
    ]
    ```

---

### Script 2: El Conector de la Alianza (Circle Matcher)
*Este script lo ejecuta Antonio en su computadora.*

*   **Entrada:** Los archivos `warm_contacts_[nombre].json` de todos los participantes.
*   **Procesamiento:**
    1.  Une todas las listas de contactos.
    2.  **Detección de Coincidencias de Compañía (Overlaps):** Agrupa los contactos por empresa para identificar en cuáles compañías hay más de un puente cálido disponible en el grupo (ej. *"Nu México: Antonio tiene de contacto a Armando Herrera (CEO) y Fernando tiene a Sofía (Director de Marketing)"*).
    3.  **Buscador Semántico:** Permite buscar por industria o cargo entre la red consolidada de los 5 amigos.
*   **Salida:** Un archivo HTML interactivo (`dashboard_alianza.html`) para que el grupo explore visualmente su red colectiva, filtre por país y genere solicitudes de introducción personalizadas.
