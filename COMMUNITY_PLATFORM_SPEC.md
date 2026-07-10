# Especificación de Producto: Plataforma de Inteligencia Relacional P2P (WhatsApp Circle)

Este documento detalla el diseño de una plataforma comunitaria privada que funciona como un "directorio inteligente de relaciones", diseñado para sustituir la búsqueda ineficiente de contactos en grupos de WhatsApp mediante la agregación voluntaria de redes de LinkedIn (BYOD).

---

## 1. El Problema Conductual (La Fricción de WhatsApp)
En comunidades de ventas, startups o sectores especializados (como Fintech/eCommerce), es habitual ver mensajes diarios en grupos de WhatsApp como:
*   *“¿Alguien tiene contacto con el CFO de Kushki?”*
*   *“¿Quién nos puede abrir la puerta en Mercado Libre?”*

Este comportamiento demuestra dos cosas:
1.  **Hay demanda activa:** La gente confía y prefiere el puente relacional sobre el correo frío.
2.  **El canal es ineficiente:** El mensaje se pierde en el feed del chat, depende de que la persona indicada lo lea en ese minuto, y no genera un histórico de relaciones estructurado. Además, **los miembros del grupo de WhatsApp no están todos conectados entre sí en LinkedIn**, por lo que sus redes individuales son invisibles para el grupo.

---

## 2. La Solución: "El LinkedIn Privado del Círculo" (Community Relational Hub)

El objetivo es crear una plataforma donde los miembros de un círculo de confianza (como un grupo de WhatsApp) puedan consolidar sus contactos de LinkedIn de forma automatizada y estructurada para buscar puentes sin violar la privacidad.

```
[ Miembro del Círculo ] ──► Busca "Nu México" ──► [ Plataforma de Círculo ]
                                                            │ (Cruce de Monederos)
                                                            ▼
                                               [ Coincidencia Encontrada ]
                                                            │
                                                            ▼
                                               "Tu amigo Antonio tiene el contacto directo de
                                                Armando Herrera (CEO). Pídele la intro aquí."
```

### Mecánica de Ingesta y Seguridad (Legal BYOD):
*   **La Barrera Legal de LinkedIn:** LinkedIn prohíbe el scraping masivo de su plataforma para crear bases de datos competidoras (riesgo de demandas por violación de T&C).
*   **El Escudo Legal (Portabilidad de Datos):** La plataforma no realiza scraping público. Funciona bajo el modelo **BYOD (Bring Your Own Data)**. Los miembros suben voluntariamente su ZIP de LinkedIn o usan la extensión personal para sincronizar sus contactos. Legalmente, el usuario es dueño de sus datos y tiene derecho a portarlos (GDPR / CCPA).
*   **Privacidad Selectiva:** Los contactos de cada usuario se mantienen en un monedero encriptado. El resto del grupo **no puede ver la lista de contactos completa de los demás**. La plataforma solo revela la coincidencia cuando un miembro busca activamente una empresa o cargo específico.

---

## 3. Flujo de Trabajo en la Plataforma

1.  **Registro y Enlace:** Los miembros de un grupo o comunidad se registran en la plataforma y se unen al círculo *"Fintech CDMX"* o *"LATAM Commerce"*.
2.  **Sincronización:** Cada miembro sube su CSV/ZIP de conexiones de LinkedIn una vez al mes o activa la sincronización local en segundo plano.
3.  **Búsqueda Directa:** Cuando un miembro necesita entrar a una cuenta, digita el nombre de la empresa en la plataforma.
4.  **Match de Confianza:** La plataforma revela la ruta de acceso: *"Antonio Gutiérrez (Clip) es conexión directa de Armando Herrera (CEO de Nu México)"*.
5.  **Solicitud y Tracking:** El sistema automatiza la petición a través de la app o notifica por WhatsApp al conector, llevando el control de la introducción y el posterior favor comercial o pago de comisión.

---

## 4. Retos Técnicos para el Equipo (José & Juan)
*   **Data Parsing Semántico:** Limpiar y estandarizar nombres de empresas y cargos que vienen de diferentes fuentes y con ortografía sucia.
*   **Criptografía y Privacidad (Zero-Knowledge Match):** Asegurar que las bases de datos de conexiones individuales no sean visibles en texto plano en el servidor central, utilizando cruzamiento de hashes.
