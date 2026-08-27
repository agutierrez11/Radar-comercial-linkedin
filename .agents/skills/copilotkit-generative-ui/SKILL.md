---
name: copilotkit-generative-ui
description: Construcción de asistentes agénticos y Copilotos con Generative UI (basado en CopilotKit/CopilotKit + MagicUI). Permite a los agentes renderizar componentes interactivos dinámicos, gráficos y modales en vivo dentro del dashboard.
---

# CopilotKit Generative UI Skill — Interfaces Generativas e Interactivas

Esta habilidad proporciona las pautas para integrar **Copilotos Agénticos** capaces de interactuar directamente con la interfaz del usuario, modificando el estado del frontend, renderizando componentes interactivos en tiempo real y desplegando widgets dinámicos (Generative UI).

---

## 🎯 Concepto Clave: De Texto Plano a UI Viva

En lugar de responder únicamente con texto en un chatbox, el copiloto agéntico renderiza componentes UI enriquecidos:
- Si el usuario dice: *"Muéstrame los mejores 5 prospectos en Cancún con cargo de VP"*, el copiloto renderiza una **Tarjeta de Prospectos Interactiva con botón de 1-clic para copiar el DM**.
- Si el usuario dice: *"Calcula cuánto me costaría enriquecer mis 5,000 contactos"*, el copiloto renderiza la **Calculadora Dinámica de Créditos BYOK**.

---

## 🛠️ Patrón de Componentes Generativos (React / Vanilla JS)

```jsx
import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";

export function ProspectDashboard({ contacts }) {
  // 1. Proporcionar contexto del estado actual al Copiloto
  useCopilotReadable({
    description: "Lista de contactos filtrados en la bóveda actual",
    value: contacts,
  });

  // 2. Definir una acción que renderiza UI dinámicamente
  useCopilotAction({
    name: "filterAndDisplayProspects",
    description: "Filtra los contactos por cargo y ubicación y los muestra en una tarjeta destacada",
    parameters: [
      { name: "titleQuery", type: "string", description: "Cargo a filtrar" },
      { name: "locationQuery", type: "string", description: "Ubicación a filtrar" }
    ],
    render: ({ status, args }) => {
      return (
        <div className="bg-slate-900 border border-violet-500/30 p-4 rounded-xl shadow-2xl">
          <h4 className="text-violet-400 font-semibold mb-2">🎯 Prospectos Filtrados: {args.titleQuery}</h4>
          <p className="text-xs text-slate-400">Estado de procesamiento: {status}</p>
        </div>
      );
    },
    handler: async ({ titleQuery, locationQuery }) => {
      // Modifica el estado global del frontend de forma transparente
      applyFilters(titleQuery, locationQuery);
    },
  });

  return <div>{/* Dashboard UI */}</div>;
}
```

---

## 🎨 Principios Estéticos y Micro-interacciones (MagicUI / Tailwind)

1. **Dark Mode por Defecto:** Fondo base Slate 950 (`#020617`), bordes luminosos subtle glassmorphism (`border-white/10`).
2. **Tipografía Curada:** Google Fonts `Outfit` para títulos y `JetBrains Mono` para datos cuantitativos y contadores de TPV.
3. **Transiciones Físicas:** Uso de `cubic-bezier(0.4, 0, 0.2, 1)` para apertura de modales y renderizado fluido de tarjetas generadas por la IA.
