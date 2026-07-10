# El Sistema de "Temperatura Relacional" (FOMO Personal para Fase 1 B2C)

Este documento detalla la lógica de gamificación, urgencia y alertas para la **Fase 1 (B2C / Uso Personal y Privado)**. Dado que en esta fase el comercial opera solo con su propia base de contactos (sin compartir datos con otros), el sistema de urgencia y el semáforo se enfocan en la **frecuencia de interacción y enfriamiento de sus propias relaciones (Data Decay)**.

---

## 1. Disparadores Psicológicos: El FOMO de la Relación Olvidada

Para un usuario individual, el FOMO no viene de la competencia con sus compañeros, sino del **enfriamiento y pérdida de valor de su propia red**.

El sistema utiliza alertas automáticas basadas en la fecha de la última interacción (extraída de su `Messages.csv` de LinkedIn):

### A. Alertas de Enfriamiento de Leads (Urgencia de Reactivación)
Cuando el comercial tiene cuentas objetivo cargadas, el sistema escanea sus chats pasados y le muestra alertas de urgencia personal:
*   *“Peligro de Enfriamiento ❄️: Chateaste con Armando Herrera (CEO de Nu) hace 85 días. La efectividad de una reconexión cae un 60% si dejas pasar más de 90 días sin hablar.”*
*   *“Ventana de Oportunidad ⚡: Este contacto está respondiendo activamente mensajes en LinkedIn esta semana según promedios del sector. ¡Escríbele hoy!”*

### B. Prueba Social de Conversión Sectorial (Datos de Mercado Anonimizados)
*   *“Métricas de Éxito 🎯: Los pitcheos del sector Fintech en México están teniendo una tasa de respuesta del 45% esta semana usando el Gancho de Valor (Estrategia B).”*
*   **Efecto:** Motiva al comercial a usar el generador de pitches de la herramienta sabiendo que está alineado con la tendencia del mercado en tiempo real.

---

## 2. El Semáforo de Temperatura Relacional (Fase 1)

En lugar de controlar la saturación de un grupo, el semáforo para el comercial individual califica **qué tan "caliente" o "fría" está su relación** con el contacto para saber qué tipo de pitch enviar:

```
[ Análisis de Conversaciones Pasadas ]
                   │
                   ▼
  [ ¿Cuándo fue el último mensaje? ]
                   │
         ┌─────────┼─────────┐
         ▼ <30 días  ▼ 30-90 días ▼ >90 días / Sin chat
    [ Verde: Warm ] [ Amarillo: Warm-Cold ] [ Rojo: Cold ]
```

*   **Ruta Verde (Warm / Caliente):** 
    *   *Criterio:* Intercambiaron mensajes hace menos de 30 días.
    *   *Acción del Sistema:* Permite un pitch directo de ventas/conversión (Estrategia A: Corto/Directo). El contacto te recuerda perfectamente.
*   **Ruta Amarilla (Warm-Cold / Templado):** 
    *   *Criterio:* Último contacto hace 30 a 90 días.
    *   *Acción del Sistema:* Sugiere un pitch de reactivación suave (Estrategia B: Aportar Valor / Enviar un PDF/Reporte) para "calentar" la relación antes de vender.
*   **Ruta Roja (Cold / Frío o Sin Interacción Pasada):** 
    *   *Criterio:* Sin chats previos en el ZIP o último mensaje hace más de 90 días.
    *   *Acción del Sistema:* Sugiere un pitch estrictamente de networking o reconexión genérica. Advertencia: *"No intentes vender de inmediato; la probabilidad de rebote es del 85%"*.

---

## 🚀 Evolución del Semáforo a Fase 2 (B2B Corporativo)

*(Nota: Este módulo se bloquea hasta la transición corporativa)*

Una vez que la empresa adquiere licencias grupales (Fase 2), este mismo semáforo evoluciona para controlar la **Saturación Colectiva**:
*   Evita que dos vendedores de la misma empresa contacten al mismo directivo en la misma semana.
*   Bloquea solicitudes duplicadas para proteger el activo de confianza de la organización.

