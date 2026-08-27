---
name: llm-council
description: Orchestrates a technical multi-LLM/multi-agent deliberation council (Andrej Karpathy methodology) for software architecture, code reviews, and technical decision making.
---

# LLM Council — Consejo Técnico de Arquitectura & Código (Karpathy Methodology)

Esta skill ejecuta el sistema de deliberación anónima multi-modelo creado por **Andrej Karpathy** enfocado en tomar decisiones técnicas complejas (*Build vs Buy*, elección de base de datos, refactorización de código, patrones de diseño).

---

## 🏛️ Estructura del Consejo Técnico

1. **Etapa 1: Recolección Ciega de Opiniones (Blind Opinion Collection):** Múltiples modelos (Claude 3.5 Sonnet, GPT-4o, Gemini 2.5 Pro, DeepSeek R1) evalúan de forma independiente el problema técnico sin conocer la opinión de los demás.
2. **Etapa 2: Revisión Anónima entre Pares (Peer Review):** Evaluación cruzada anonimizada (`Modelo A`, `Modelo B`, `Modelo C`) buscando fallas de arquitectura, problemas de escala o cuellos de botella de memoria/rendimiento.
3. **Etapa 3: Síntesis del Presidente (Chairman Verdict):** El Presidente del Consejo entrega la solución técnica consolidada definitiva.

---

## 💡 Cómo Invocar este Consejo
- `"Ejecuta el LLM Council para auditar la arquitectura de mi API"`
- `"/teamwork-preview Corre el LLM Council para evaluar esta decisión de base de datos"`
