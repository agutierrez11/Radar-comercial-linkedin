---
name: ab-test-behavioral-analytics
description: Framework técnico ejecutable para Pruebas A/B, análisis de significancia estadística conductual (Chi-cuadrado, p-value, Z-score) y segmentación por clústeres K-Means en Python para optimizar campañas de prospección B2B.
version: 1.0.0
---

# 📊 AB Test & Behavioral Analytics (Skill Técnico Ejecutable)

Este skill contiene los scripts en Python listos para correr en terminal para evaluar científicamente pruebas A/B de mensajes/correos y segmentar automáticamente a los contactos de la Bóveda por afinidad conductual.

---

## 🚀 1. Analizador de Pruebas A/B (`scripts/analyze_ab_test.py`)

Calcula si la diferencia en tasa de apertura o agendamiento entre Variante A y Variante B es **estadísticamente significativa** ($p < 0.05$).

### Uso en Terminal:
```bash
python .agents/skills/ab-test-behavioral-analytics/scripts/analyze_ab_test.py --sent_a 500 --conv_a 25 --sent_b 500 --conv_b 48
```

---

## 🧩 2. Clustereador Conductual K-Means (`scripts/behavioral_cluster.py`)

Segmenta automáticamente a los contactos de `master_data.js` / `enriched_connections.json` en 4 grupos estratégicos según su jerarquía, calidez y canal de contacto.

### Uso en Terminal:
```bash
python .agents/skills/ab-test-behavioral-analytics/scripts/behavioral_cluster.py
```
