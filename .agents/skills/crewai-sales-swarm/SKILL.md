---
name: crewai-sales-swarm
description: Orquestación de equipos agénticos de ventas B2B multi-rol con CrewAI (Researcher + Scorer + Trigger Analyst + Copywriter). Diseñado para prospección autónoma y campañas de alta conversión.
---

# CrewAI Sales Swarm Skill — Enjambre Agéntico de Ventas B2B

Esta habilidad permite estructurar y ejecutar enjambres agénticos multi-rol utilizando el patrón de arquitectura de **CrewAI**, coordinando agentes autónomos para investigar cuentas objetivo, cualificar leads por ICP y redactar campañas comerciales.

---

## 🛠️ Estructura del Equipo (Roles & Tareas)

1. **ICP Researcher:** Explora y extrae información pública de la empresa (tamaño, geografía, stack tecnológico).
2. **Account Qualifier:** Asigna puntuación de encaje ICP (0 a 100) y filtra falsos positivos.
3. **Trigger Event Miner:** Detecta noticias recientes, contratación de personal clave y expansiones.
4. **Outbound Copywriter:** Redacta copys fríos hiper-personalizados bajo metodologías MEDDIC / Challenger Sale.

---

## 📋 Configuración del Crew en Python

```python
from crewai import Agent, Crew, Process, Task

researcher = Agent(
    role='Lead Researcher',
    goal='Extraer la metadata clave y stack tecnológico de la empresa objetivo',
    backstory='Experto en inteligencia comercial B2B y scraping web de cuentas enterprise.'
)

copywriter = Agent(
    role='Outbound Copywriter',
    goal='Redactar una secuencia de 3 correos fríos hiper-personalizados para el VP de Pagos',
    backstory='Especialista en ventas B2B Fintech y metodologías MEDDIC/Challenger Sale.'
)

task1 = Task(description='Investigar la cuenta objetivo Mercado Pago México', agent=researcher)
task2 = Task(description='Redactar el pitch de reducción de comisiones vía API', agent=copywriter)

sales_crew = Crew(
    agents=[researcher, copywriter],
    tasks=[task1, task2],
    process=Process.sequential
)
```
