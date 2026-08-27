---
name: llm-council
description: Orchestrates a multi-LLM/multi-agent deliberation council (Andrej Karpathy methodology) with blind response collection, peer review, and a Chairman synthesis.
---

# LLM Council — Sistema de Deliberación Multi-Modelo & Multi-Agente (Framework Maestro)

Esta skill implementa la metodología **5-LLM Council** (creada por Andrej Karpathy) para auditar estrategias comerciales, validar arquitectura de productos o evaluar decisiones de negocio reduciendo sesgos de complacencia.

---

## 👥 Matriz de Roles de los 5 LLMs (Framework Agnóstico)

| ID | Modelo Principal | Rol Especializado | Ángulo de Análisis |
| :--- | :--- | :--- | :--- |
| **Modelo A** | **Claude 3.5 Sonnet** | **Arquitectura de Producto & Copywriting B2B** | Evalúa la propuesta de valor, mensajes de prospección y experiencia de integración API. |
| **Modelo B** | **GPT-4o** | **Métricas Comerciales & Pipeline RevOps** | Evalúa unit economics, ROI esperado, velocidad de venta (Speed to Sell) y tasas de conversión. |
| **Modelo C** | **Gemini 2.5 Pro** | **Estrategia Macro, Mercado & Compliance** | Evalúa regulaciones regionales, tamaño de mercado (TAM/SAM) y contexto legal. |
| **Modelo D** | **DeepSeek V3 / R1** | **Auditoría Adversaria & Gestión de Riesgos** | Actúa como *Abogado del Diablo*; busca vulnerabilidades de seguridad y fallas operativas. |
| **Modelo E** | **Kimi / Manus** | **Ecosistema, Integraciones & Co-Selling** | Evalúa alianzas de software, APIs de terceros y estrategias de co-selling. |

---

## 🏛️ Las 3 Etapas del Consejo

### 1. Etapa 1: Recolección Ciega de Opiniones (Blind Opinion Collection)
Se toma la consulta del usuario y se envía aisladamente a los 5 modelos o subagentes.
- Cada participante genera su respuesta de manera **autónoma e independiente**, sin conocer las respuestas de los otros miembros.

### 2. Etapa 2: Revisión Anónima entre Pares (Peer Review)
Se distribuyen las respuestas de la Etapa 1 a todos los miembros del consejo de forma **anonimizada** (`Modelo A`, `Modelo B`, `Modelo C`, `Modelo D`, `Modelo E`).
- Cada modelo evalúa las propuestas de los demás buscando suposiciones no probadas, riesgos de ejecución o puntos ciegos.

### 3. Etapa 3: Síntesis del Presidente del Consejo (Chairman Synthesis)
El modelo designado como **El Presidente (Chairman)** compila todas las opiniones y entrega un **Informe Consolidado Final** con los 3 Pilares de Defensa Blindada.
