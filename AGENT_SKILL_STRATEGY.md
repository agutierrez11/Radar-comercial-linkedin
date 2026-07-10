# Estrategia de Distribución: Radar Comercial como "Agentic Skill" (MCP / API)

Este documento detalla el modelo de distribución de **Radar Comercial como una Skill de Inteligencia Artificial (Agentic Skill)** para plataformas de agentes empresariales (Gemini Enterprise, Vertex AI, Claude Enterprise), acelerando la venta, eliminando el costo de desarrollo de interfaces (UI) y montándonos sobre la ola de adopción de agentes de IA en corporativos.

---

## 1. ¿Qué es una "Agentic Skill" en este contexto?

En lugar de vender Radar Comercial como un SaaS tradicional (una página web a la que el usuario debe entrar y aprender a usar), empaquetamos la lógica del producto como una **habilidad instalable para Agentes de Inteligencia Artificial**:

*   **El Formato:** Un servidor MCP (Model Context Protocol) o un endpoint de API estructurado que se registra en la plataforma de agentes de la empresa (ej. Gemini Enterprise Agent Platform).
*   **Las Herramientas Expuestas:**
    1.  `parse_connections_data`: Herramienta para procesar el CSV/ZIP de conexiones.
    2.  `match_crm_targets`: Herramienta para cruzar contactos contra cuentas objetivo.
    3.  `generate_localized_pitch`: Generar el copy con el gancho según geografía e ICP.

---

## 2. ¿Por qué este modelo se vende e integra 10x más rápido?

### A. Cero Fricción de Interfaz (No UI Overhead)
No tienes que diseñar, programar ni dar mantenimiento a complejas aplicaciones web o extensiones de navegador. El "frontend" es el chat o el agente que la empresa ya utiliza (ej. Slack, Teams o su chatbot interno).
*   **Ejemplo de uso:** El comercial simplemente le chatea a su copiloto de IA corporativo: *"Oye, necesito entrar a Nu México. Revisa en el módulo de Radar Comercial si tenemos algún puente cálido."* El agente invoca la Skill en segundo plano y responde en el chat: *"Sí, Antonio Gutiérrez conoce al CEO Armando Herrera. ¿Quieres que redacte la solicitud de introducción?"*

### B. Aprobación de TI Corporativa Ultra Rápida
Conseguir que el departamento de seguridad de una empresa apruebe la instalación de una nueva plataforma de software externa puede tardar meses. Aprobar una "Skill" o una conexión de API bajo un entorno seguro existente (como Google Cloud / Vertex AI) es un proceso infinitamente más rápido y sencillo.

### C. Distribución a través de Marketplaces / Registros
Las empresas tecnológicas están creando **Registros de Skills** (como el *Agent Platform Skill Registry*). Al registrar nuestra Skill en estos catálogos:
*   Cualquier empresa que ya use agentes de IA puede "descargar" y activar Radar Comercial en un clic.
*   Nos montamos sobre la fuerza de venta de los grandes proveedores de nube (Google Cloud, AWS) quienes promueven nuestro software porque aumenta el consumo de sus propias plataformas de IA.

---

## 3. Beneficios Técnicos para José y Juan

Este enfoque entusiasmará a tu equipo de desarrollo:
*   **Foco en el Core:** José (Data Scientist) y Juan (Data Engineer) no tienen que preocuparse por crear layouts HTML, CSS, logins de usuarios o cookies. Su único foco es programar el **algoritmo de grafos y limpieza de datos en Python**, exponerlo como un microservicio (API) y estructurar las instrucciones del prompt para el agente.
*   **Arquitectura Moderna:** El código se vuelve modular, mantenible y listo para la era de la computación agentica.
