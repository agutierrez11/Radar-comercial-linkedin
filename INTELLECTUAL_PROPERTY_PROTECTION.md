# Protección de Propiedad Intelectual y Control de Monetización en la Skill

Este documento técnico detalla cómo protegemos nuestro código y aseguramos la monetización recurrente (SaaS) al empaquetar Radar Comercial como una Skill, evitando que los usuarios copien la lógica o la utilicen de forma gratuita.

---

## 1. La Arquitectura "Thin Client / Thick Backend" (Cliente Ligero / Servidor Robusto)

Para evitar perder el control del software, la Skill que el usuario instala en su agente de IA no contiene los algoritmos ni la lógica de negocio. Es simplemente un **conector seguro** (un cascarón):

```
[ Agente del Cliente (Gemini/Claude) ]
                 │
                 ▼ (Invocación de Herramienta)
   [ Skill de Radar (Cliente Ligero) ] ──► Envía datos encriptados + API Key
                 │
                 ▼ (HTTPS Seguro)
   [ API de Radar Comercial (Servidor Cerrado) ] ──► Valida Pago y ejecuta algoritmos (José/Juan)
                 │
                 ▼ (Retorna Resultado)
[ Agente recibe la respuesta y la muestra ]
```

1.  **La Skill Local (Cliente Ligero):** Es un archivo JSON/YAML público que describe las herramientas (ej. "Esta herramienta procesa un archivo"). No contiene código ejecutable sensible, solo especifica a qué servidor llamar.
2.  **La API Corporativa (Servidor Cerrado):** Los algoritmos de inferencia geográfica, la limpieza de nombres de José y el cálculo de scores relacionales corren estrictamente en **nuestros servidores privados**. Ningún cliente tiene acceso a este código.

---

## 2. Control de Acceso y Facturación (Monetización Segura)

El acceso a la Skill se controla de la misma forma que cualquier SaaS moderno:

*   **API Key obligatoria:** Para activar la Skill, el agente del usuario debe enviar una clave de API única (`RC_API_KEY`) en cada consulta.
*   **Validación de Suscripción:** Nuestro servidor recibe la consulta, verifica en nuestra base de datos si la clave de API está asociada a una cuenta activa en Stripe (pago al corriente de $10 USD/mes).
*   **Bloqueo Automático:** Si el usuario cancela su suscripción o su pago rebota, el servidor responde con un error `401 Unauthorized`. El agente de IA del cliente mostrará un mensaje: *"Tu licencia de Radar Comercial no está activa. Actívala o renuévala aquí: [Enlace]"*.

---

## 3. Ventajas para la Startup

*   **Control del IP:** Aunque el usuario intente copiar la Skill de un agente a otro, no podrá usarla sin una clave de API válida y de pago.
*   **Actualizaciones Invisibles:** Podemos actualizar los algoritmos de IA de José o las plantillas de pitcheo en nuestro servidor en cualquier momento, y todos los usuarios recibirán las mejoras de inmediato sin necesidad de reinstalar nada en sus agentes.
*   **Métricas de Uso:** Al pasar las solicitudes por nuestro servidor, podemos medir exactamente cuántas llamadas hace cada usuario para limitar el uso por niveles de precio (ej. Plan Básico: 100 consultas/mes, Plan Pro: ilimitado).
