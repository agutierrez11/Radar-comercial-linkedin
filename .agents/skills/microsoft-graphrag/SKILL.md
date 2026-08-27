---
name: microsoft-graphrag
description: RAG basado en Grafos de Conocimiento impulsado por Microsoft GraphRAG (microsoft/graphrag). Extrae entidades, jerarquías y comunidades de relaciones en datos B2B no estructurados.
---

# Microsoft GraphRAG Skill — Retrieval-Augmented Generation en Grafos

Esta habilidad permite estructurar documentos y mensajes no estructurados en un **Grafo de Conocimiento Semántico**, agrupando entidades por comunidades de influencia para responder consultas complejas de redes B2B.

---

## 🔍 Diferencia con RAG Vectorial Tradicional

| RAG Vectorial Plano | GraphRAG (Microsoft) |
| :--- | :--- |
| Busca similitud semántica por trozos aislados (*chunks*). | Conecta entidades (Personas ➔ Cargos ➔ Empresas ➔ Sectores) en una red interconectada. |
| No entiende jerarquías globales ni relaciones implícitas. | Detecta comunidades de influencia y resume la red completa. |
