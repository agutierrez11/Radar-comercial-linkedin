---
name: scoring
description: |
  Úsala cuando tienes una lista de gente que comentó los posts de tus creadores vigilados y no sabes a quién escribir primero. Puntúa cada uno por encaje con tu cliente ideal y por intención, devolviendo la lista ordenada con el motivo de cada posición.
---

# Scoring de Encaje e Intención

## Lógica
1. Descarta a los perfiles fuera de ICP antes de puntuar (según `modelador-de-icp`).
2. Evalúa dos dimensiones:
   - **Intención:** Sustancia del comentario (comentario reflexivo con problema real vs "gracias por compartir") + Autoridad del cargo.
   - **Tamaño de la oportunidad:** Tamaño de empresa y encaje de la cuenta.
3. Cruza ambas variables en la Matriz de Priorización:
   - **Alto:** Cargo Decisor + Intención Fuerte.
   - **Medio:** Cargo Decisor + Intención Débil O Influyente + Intención Fuerte.
   - **Bajo:** Cargo no decisor o comentario superficial.
4. **Cruce de Red Cálida (Exclusivo Radar Comercial):** Si el prospecto ya es conexión de 1er grado o tiene puente interno, eleva automáticamente a la categoría de Máxima Prioridad Cálida.
5. Aplica decaimiento perezoso (el score de un prospecto de nivel Alto baja a Medio tras 60 días sin señales nuevas).
