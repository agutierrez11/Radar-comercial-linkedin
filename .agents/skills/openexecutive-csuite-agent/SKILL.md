---
name: openexecutive-csuite-agent
description: Framework de Orquestación Agéntica Ejecutiva C-Suite (basado en SenteLabsAI/OpenExecutive). Equipo ejecutivo virtual unificado con 8 especialistas (CFO, CSO, CMO, COO, GC, CHRO, CPO) y reportes en lenguaje natural.
---

# OpenExecutive C-Suite Agent Skill — Orquestador Ejecutivo Virtual

Esta habilidad integra la arquitectura técnica de **SenteLabsAI/OpenExecutive** para la operación de un equipo directivo virtual unificado que reporta directamente al usuario en lenguaje humano (sin consola de comandos).

---

## 🛠️ Arquitectura y Roles Especializados

```mermaid
graph TD
    U[👑 Antonio / Usuario CEO] <--> E[👔 The Executive Orchestrator]

    subgraph ESPECIALISTAS ["👥 8 Especialistas Directivos"]
        E --> CSO["CSO (Estrategia & M&A)"]
        E --> CFO["CFO (Finanzas & Modelo)"]
        E --> CMO["CMO (Marketing & GTM)"]
        E --> COO["COO (Operaciones & Procesos)"]
        E --> GC["GC (Legal & Cumplimiento)"]
        E --> CHRO["CHRO (Talento & Organización)"]
        E --> CPO["CPO (Producto & Roadmap)"]
        E --> BOARD["Board Comms (Reportes Ejecutivos)"]
    end
```

---

## 🚀 Características Clave

1. **Voz Ejecutiva Unificada:** El usuario solo interactúa con un Orquestador Ejecutivo que delega internamente en paralelo a los especialistas mediante llamadas `asyncio.gather`.
2. **Reportes Ejecutivos en Lenguaje Natural:** Cero logs de terminal; comunicación ejecutiva diaria vía Telegram, Slack o WhatsApp.
3. **Memoria Episódica en SQLite + ChromaDB:** Persistencia total de decisiones, KPIs corporativos y contexto de negocio.
