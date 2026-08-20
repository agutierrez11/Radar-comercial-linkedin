---
name: clasificador-de-senales-de-dm-de-linkedin
description: |
  v2. Clasifica las respuestas entrantes a tus invitaciones de outreach en LinkedIn y las categoriza para evitar que los prospectos cálidos se enfríen en la bandeja de entrada.
---

# Clasificador de Señales de DM de LinkedIn

## Lógica
1. Lee las conversaciones entrantes de LinkedIn y enruta cada hilo en exactamente una de las 6 categorías:
   - 🟢 **INTERESADO:** Solicita el recurso, realiza preguntas concretas o muestra intención clara.
   - ❓ **PREGUNTA:** Pide aclaraciones o contexto adicional sobre la propuesta.
   - ⏳ **NO_AHORA:** Muestra interés pero solicita retomar la conversación en el futuro.
   - 🔴 **NO_INTERESA:** Rechaza explícitamente la interacción.
   - 📥 **SPAM_O_VENTA:** Intento de venta entrante (pitch invertido).
   - ⚪ **SIN_CLASIFICAR:** No encaja en las anteriores (requiere revisión manual).
2. **Respuesta Sugerida:** Para perfiles INTERESADO o PREGUNTA, redacta un borrador de respuesta sugerida anclado al hilo de la conversación.
3. **Persistencia del Histórico:** Actualiza la base de datos de contacto para evitar repeticiones o repuntuaciones de prospectos que ya están en conversación activa.
