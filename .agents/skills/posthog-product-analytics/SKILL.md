---
name: posthog-product-analytics
description: Integración de telemetría de uso, mapas de calor, grabación de sesiones, Feature Flags para A/B testing y medición de conversión de productos B2B (basado en posthog/posthog).
---

# PostHog Product Analytics Skill — Telemetría & Experimentación B2B

Esta habilidad establece los patrones de instrumentación para capturar el comportamiento real del usuario dentro de la aplicación, medir la adopción de features clave, realizar pruebas A/B con Feature Flags y alimentar el pipeline de métricas de **Revenue Operations (RevOps)**.

---

## 🎯 Objetivos de Telemetría (Radar Comercial & SaaS)

1. **Embudo de Conversión (Funnel):**
   - `User Registered` ➔ `ZIP Data Uploaded` ➔ `Contacts Processed` ➔ `Warm Intro Requested` ➔ `Deal Closed`.
2. **Adopción de Features Core:**
   - Medir frecuencia de uso del filtro de cargos, búsquedas por TPV, uso de la calculadora de créditos BYOK y exportaciones a CSV/CRM.
3. **Pruebas A/B (Feature Flags):**
   - Comparar variantes de interfaz (ej. Vista A vs Vista B del Dashboard de Analytics o Modal de Bienvenida).

---

## 🛠️ Snippet de Inicialización en Frontend (Vanilla JS / React)

```javascript
import posthog from 'posthog-js';

// Inicialización de PostHog
export function initAnalytics() {
    posthog.init('YOUR_POSTHOG_API_KEY', {
        api_host: 'https://app.posthog.com',
        autocapture: true,
        capture_pageview: true,
        persistence: 'localStorage',
        disable_session_recording: false
    });
}

// Rastreo de Eventos Clave de Negocio
export function trackVaultUpload(contactCount, isDemo = false) {
    posthog.capture('vault_data_loaded', {
        total_contacts: contactCount,
        is_demo: isDemo,
        timestamp: new Date().toISOString()
    });
}

export function trackWarmIntroRequest(targetContactId, targetCompany) {
    posthog.capture('warm_intro_requested', {
        contact_id: targetContactId,
        company: targetCompany
    });
}
```

---

## 🔒 Reglas de Privacidad y Cumplimiento

1. **Zero PII Leakage:** Nunca enviar PII sensible (números de teléfono personales, contraseñas o contenido encriptado de mensajes privados) a los servidores de analytics.
2. **Masking:** Aplicar máscaras automáticas en las grabaciones de sesión (`posthog-mask`) sobre campos de datos confidenciales.
3. **Respeto a la Bóveda Privada:** Registrar únicamente los eventos de acción del usuario (clics, navegación, uso de filtros) sin almacenar el contenido de la red del usuario.
