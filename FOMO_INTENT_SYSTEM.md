# El Sistema FOMO y Semáforo de Saturación de Contactos

Este documento detalla la lógica de gamificación, urgencia y coordinación basada en **FOMO (Fear Of Missing Out / Miedo a Quedarse Fuera)** y alertas de saturación para optimizar la tasa de respuesta en prospección B2B.

---

## 1. Disparadores Psicológicos: El FOMO del Vendedor

Los comerciales son perfiles competitivos por naturaleza. El sistema utiliza notificaciones de actividad en tiempo real e histórica para impulsar la acción inmediata:

### A. Alerta de Competencia en Cuentas Objetivo
Cuando un comercial busca una empresa (ej. Nu México) o la tiene en su pipeline, el sistema le muestra indicadores de demanda:
*   *“Fuego 🔥: 4 comerciales en tu círculo de alianza buscaron contactos en Nu México en las últimas 48 horas.”*
*   *“Urgencia ⚡: Esta cuenta es prioritaria. 2 de tus aliados tienen rutas directas de 1er grado activas hoy.”*
*   **Efecto:** El vendedor siente urgencia de solicitar la introducción de inmediato antes de que otro comercial de su alianza o competencia gane la cuenta o sature los puentes de confianza.

### B. Prueba Social de Conversión
*   *“Casos de Éxito 🎯: Hace 3 horas, un comercial cerró una reunión con el CFO de Clip usando un puente de confianza de Antonio Gutiérrez.”*
*   **Efecto:** Valida el valor de la herramienta y motiva al usuario a seguir minando y enriqueciendo sus contactos.

---

## 2. El Semáforo de Saturación (Proteger el Activo de Confianza)

El mayor riesgo de un sistema de introducciones es el **spam**. Si 5 vendedores del mismo círculo o empresa intentan llegar al CEO Armando Herrera la misma semana, van a quemar el contacto, Antonio perderá su relación de confianza y la plataforma perderá credibilidad.

Para evitar esto, el sistema FOMO convive con un **Semáforo de Saturación (Outbound Frequency Cap)**:

```
[ Solicitud de Intro a Armando Herrera ]
                   │
                   ▼
  [ ¿Recibió solicitudes recientes? ]
                   │
         ┌─────────┴─────────┐
         ▼ SI                ▼ NO
[ Alerta de Saturación ]    [ Ruta Verde: Permitir Intro ]
- "Armando ya recibió una intro hoy"
- "Espera 72 horas para no quemar el contacto"
- "Opción: Súmate al deal de tu colega"
```

*   **Ruta Verde (Libre):** El contacto no ha sido buscado ni contactado recientemente. El vendedor puede proceder de inmediato.
*   **Ruta Amarilla (Precaución):** *"Armando Herrera recibió una solicitud de intro hace 3 días. Su tasa de respuesta histórica es alta. Se recomienda esperar 24 horas antes de enviar otra."*
*   **Ruta Roja (Bloqueado/Saturado):** *"Contacto Saturado. Armando Herrera ya fue contactado hoy por tu colega Fernando Estévez. Para proteger la relación de Antonio Gutiérrez, el canal está bloqueado por 72 horas. Opciones: Chatea con Fernando para sumarte al deal."*

---

## 📈 Beneficio de Negocio (Retención y Calidad)

1.  **Protección de la Red:** Los conectores (como Antonio) aceptan compartir su red porque saben que el sistema **nunca permitirá que sus contactos de confianza sean spameados**.
2.  **Fomento de la Colaboración B2B:** Fuerza a los vendedores de la misma empresa o alianza a colaborar en "deals" conjuntos en lugar de competir de forma destructiva por el mismo tomador de decisiones.
