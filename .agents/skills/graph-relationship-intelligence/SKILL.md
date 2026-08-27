---
name: graph-relationship-intelligence
description: Minería de Inteligencia de Relaciones y Grafos B2B basada en Neo4j y Microsoft GraphRAG (XD-MHLOO/Osintgraph + GraphRAG). Convierte datos de conexiones y chats planos en mapas visuales de puentes cálidos de 1er y 2º grado.
---

# Graph Relationship Intelligence Skill — Minería de Grafos B2B (Neo4j + GraphRAG)

Esta habilidad proporciona las directrices y arquitecturas para transformar datasets desestructurados (exportaciones CSV de LinkedIn, mensajes históricos de chat, notas de CRM) en un **Grafo de Conocimiento y Relaciones Conectadas** en **Neo4j** utilizando modelos RAG basados en grafos (**Microsoft GraphRAG**).

---

## 🎯 Caso de Uso Core (Radar Comercial & B2B Sales)

En la prospección tradicional, las listas de contactos son estáticas y planas. Esta habilidad permite responder preguntas de la red de relaciones como:
- *"¿Quién en mi red de 1er grado conoce al VP de Pagos o CEO de [Empresa Objetivo]?"*
- *"¿Qué contactos de mi red trabajaron previamente en Clip, Fiserv o Mercado Pago y hoy son C-Levels en otras empresas?"*
- *"¿Cuál es la ruta de introducción cálida (Warm Intro Path) con menor fricción para llegar a esta cuenta?"*

---

## 🛠️ Modelo de Datos del Grafo (Neo4j Schema)

```cypher
// Nodos Core
(:Contact {id, name, title, company, location, linkedin_url})
(:Company {name, industry, size, tech_stack})
(:Position {title_normalized, seniority_level})
(:City {name, country})
(:User {id, name}) // El vendedor / dueño de la bóveda BYOD

// Relaciones
(:Contact)-[:CURRENTLY_WORKS_AT {since}]->(:Company)
(:Contact)-[:PREVIOUSLY_WORKED_AT {duration}]->(:Company)
(:Contact)-[:HAS_ROLE]->(:Position)
(:Contact)-[:LOCATED_IN]->(:City)
(:User)-[:CONNECTED_TO_1ST_DEGREE {connected_date}]->(:Contact)
(:Contact)-[:KNOWS_2ND_DEGREE]->(:Contact)
```

---

## 🔍 Consultas de Inteligencia de Relaciones (Cypher Queries)

### 1. Encontrar Puentes Cálidos a una Empresa Objetivo

```cypher
MATCH (u:User {name: "Antonio"})-[r1:CONNECTED_TO_1ST_DEGREE]->(c1:Contact)-[r2:CURRENTLY_WORKS_AT]->(comp:Company {name: "Mercado Libre"})
RETURN c1.name AS Connector, c1.title AS Role, comp.name AS TargetCompany
ORDER BY c1.connected_date DESC;
```

### 2. Detectar la Tesis "De Becario a CEO" (Cargos Pasados vs Actuales)

```cypher
MATCH (c:Contact)-[:PREVIOUSLY_WORKED_AT]->(oldComp:Company)
MATCH (c)-[:CURRENTLY_WORKS_AT]->(newComp:Company)
MATCH (c)-[:HAS_ROLE]->(pos:Position)
WHERE pos.seniority_level IN ['VP', 'Director', 'C-Level', 'Founder']
RETURN c.name, oldComp.name AS PastCompany, newComp.name AS CurrentCompany, pos.title_normalized AS CurrentTitle;
```

---

## 🚀 Flujo de Enriquecimiento e Integración

1. **Ingesta BYOD:** El usuario sube su `Connections.csv` de LinkedIn.
2. **Normalización NLP:** Se normalizan acentos y cargos con LLMs (`LLM & NLP Engineer`).
3. **Población en Grafo:** Se crean los nodos y relaciones en la base de datos gráfica Neo4j local o en la nube.
4. **GraphRAG Reasoning:** Ante una consulta natural del comercial, GraphRAG analiza las comunidades de influencia del grafo y devuelve el **camino de introducción de mayor probabilidad de éxito**.
