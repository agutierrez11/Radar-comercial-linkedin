---
name: ai-sales-simulator
description: Simulador de guerra de ventas y gemelos digitales de buyer personas (basado en ndpvt-web/ai-sales-agent-simulator + persona-8b + prompts.chat). Simula objeciones y prueba pitches B2B antes de enviarlos a prospectos reales.
---

# AI Sales Simulator Skill — Guerra de Pitches & Gemelos Digitales de ICP

Esta habilidad permite crear **Gemelos Digitales de Buyer Personas** para simular llamadas comerciales, evaluar la efectividad de secuencias frías y predecir objeciones probables antes de iniciar una campaña de prospección real.

---

## 🎯 Método de Simulación & Sparring Comercial

1. **Definir Perfil ICP:** Asignar rol (ej. CFO enfocado en costos, VP de Operaciones escéptico, Director de Tecnología).
2. **Consultar Banco de Roles Curados:** Consultar `references/b2b_buyer_personas_prompts.md` para extraer el comportamiento y restricciones exactas de la persona.
3. **Ejecutar Sparring:** Hacer que la IA adopte la persona del comprador y responda al pitch de ventas de Kashio/Paymind con objeciones realistas.
4. **Reporte de Desempeño:** Evaluar claridad de propuesta de valor, manejo de objeciones y tasa de conversión estimada.

---

## 📚 Módulos & Referencias Instaladas

- [`references/b2b_buyer_personas_prompts.md`](file:///c:/Users/Antonio/.gemini/antigravity-ide/scratch/radar-comercial/.agents/skills/ai-sales-simulator/references/b2b_buyer_personas_prompts.md): **607 Roles Ejecutivos B2B** extraídos y curados de `f/prompts.chat` (CFO, CEO, IT Director, Sales VP, Security Auditor, Recruiter, etc.).

