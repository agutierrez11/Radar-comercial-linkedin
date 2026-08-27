---
name: apache-maka-agent-kernel
description: Registro persistente append-only y arquitectura de recuperación tras fallos (crash recovery) para agentes de IA basada en apache/maka.
---

# Apache Maka Agent Kernel Skill — Persistencia & Reorganización tras Fallos

Esta habilidad implementa el patrón de diseño de **Apache Maka** para garantizar que los agentes registren sus mensajes, llamadas a herramientas y decisiones en un log *append-only*, permitiendo reanudar la ejecución exactamente donde se quedó ante reinicios o desconexiones.

---

## 🔒 Beneficios de Arquitectura

1. **Crash Recovery:** Recompone el estado exacto del agente reejecutando la secuencia de eventos guardada.
2. **Auditoría de Herramientas:** Registro inmutable de cada acción ejecutada en el sistema.
