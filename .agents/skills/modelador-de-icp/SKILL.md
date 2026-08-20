---
name: modelador-de-icp
description: |
  Úsala para convertir una descripción en lenguaje natural de tu cliente ideal en una consulta concreta y guardada, contra la que el resto del sistema puntúa. Se activa cuando toca definir o revisar el cliente ideal de esta vigilancia: "modela mi cliente ideal", "define el cliente ideal para esta campaña", "quiero vigilar creadores para vender a [tipo de empresa o persona]".
---

# Modelador de Cliente Ideal (ICP)

## Lógica
1. Traduce tu descripción en lenguaje natural a filtros ejecutables: sector, tamaño de empresa (empleados o facturación), y cargos que deciden de verdad frente a cargos que no cuentan aunque comenten con entusiasmo.
2. Mide el volumen potencial contra la base de datos de Radar Comercial / Apollo.
3. Guarda la consulta en la base de datos del proyecto (`crm_status` / Supabase), definiendo el Suelo Duro.
4. Escribe el Suelo Duro como negación, no como aspiración: qué queda fuera sin discusión.

## Reglas del Suelo Duro
1. **Define qué cargos SÍ cuentan** (quien decide o influye la compra de verdad) y cuáles NO. Un pasante que escribe "excelente post" queda fuera.
2. **Define el tamaño mínimo y máximo** de empresa objetivo.
3. **Negación directa:** "Nunca operaciones de una sola persona" es una regla ejecutable.
4. **Actualización continua:** El suelo se corrige con casos reales que pasaron el corte y no debían.
