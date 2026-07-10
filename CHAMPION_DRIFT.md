# Alerta de Campeones en Movimiento: El Motor de Detección de Cambios de Empresa (Job Change / Account Drift)

Este documento detalla la lógica de negocio y arquitectura técnica para la funcionalidad de **Detección de Movimientos de Leads**, inspirada en el caso de Miguel Ángel Pedraza (Macropay).

---

## 1. La Oportunidad Comercial: "El Efecto Campeón"

En ventas B2B, cuando un cliente satisfecho (un "Campeón" que ya te compró en el pasado, como Miguel en Clip) cambia de empleo:

1.  **Venta Caliente en la Nueva Empresa:** El campeón llega a su nueva empresa con presupuesto y poder de decisión, y tiene una **probabilidad de compra 3 veces mayor** para tu producto actual (Toku/Netpay) porque ya confía en ti.
2.  **Cuenta en Riesgo en la Antigua Empresa:** La cuenta original (ej. Macropay) queda "huérfana" de tu contacto clave. Necesitas meter un reemplazo (comercial nuevo) para evitar perder el contrato.

---

## 2. Lógica de Inferencia de Cambios de Empresa

El sistema cruza el historial de datos estáticos con los datos del perfil actual para detectar discrepancias:

```
[ Correo Original: miguel.pedraza@macropay.mx ] 
                     VS
[ Perfil Actual en LinkedIn: Director en Oxxo ]
                     ⬇️
      [ ALERTA: CAMBIO DE EMPRESA DETECTADO ]
```

### Algoritmo de Detección:
1.  **Extracción de Dominio Base:** Extraer el dominio del correo histórico registrado (ej. `macropay.mx` -> `Macropay`).
2.  **Extracción de Empresa Actual:** Leer la empresa actual desde la extensión de Chrome o API de enriquecimiento en LinkedIn.
3.  **Comparación Semántica:**
    *   Si el dominio original no coincide con el nombre de la empresa actual (ej. `macropay` != `oxxo`), se marca como **"Drift Detectado"** (Desviación).
4.  **Cálculo de la Fecha de Salida:**
    *   Comparar la fecha de la última interacción exitosa en la empresa anterior con la fecha de inicio del cargo actual.

---

## 3. Flujo de Trabajo en Radar Comercial (MVP)

1.  **Importación Inicial:** El comercial sube sus contactos con correos corporativos (ej. `pedraza@macropay.mx`).
2.  **Monitoreo Silencioso (Chrome Extension):** Cuando la extensión visita de forma orgánica perfiles antiguos, compara la empresa en vivo con el registro.
3.  **Disparador de Alerta:**
    *   *Alerta Roja (Riesgo en Cuenta):* *"Miguel Ángel Pedraza ya no está en Macropay. Busca a su reemplazo en el área de pagos de Macropay."*
    *   *Alerta Verde (Oportunidad Nueva):* *"Miguel Ángel Pedraza ahora es Director en [Nueva Empresa]. Escríbele para presentarle Toku."*
