---
name: claw-code-agent-harness
description: Arnés y runtime de agentes de código de terminal de alto rendimiento escrito en Rust/Python (basado en ultraworkers/claw-code). Ejecución de herramientas, bucles agénticos autónomos y llamadas a APIs de LLMs.
---

# Claw Code Agent Harness Skill — Runtime Agéntico de Terminal (Rust/Python)

Esta habilidad define la arquitectura para desarrollar y desplegar arneses (*agent harnesses*) de ejecución de código en la terminal basados en la arquitectura de **Claw Code** (`ultraworkers/claw-code`).

---

## 🛠️ Componentes Principales

1. **Rust Core Runtime:** Manejo ultrarrápido de llamadas a herramientas (*tool use*), parsing de comandos de terminal, diffs de archivos y streaming de modelos.
2. **Autonomous Execution Loop:** Ciclo de pensamiento y acción con recuperación automática de errores (*self-healing loop*).
3. **Subagent Orchestration:** Despacho de subagentes paralelos para tareas de testing, refactorización y documentación.
