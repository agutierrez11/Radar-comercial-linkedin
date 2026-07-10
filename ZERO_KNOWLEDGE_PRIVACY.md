# Arquitectura Cero-Conocimiento (Zero-Knowledge Privacy) y Perfiles Lookalike

Este documento detalla el diseño ético y criptográfico para garantizar la privacidad absoluta de los datos de los comerciales. Describe cómo funciona la recomendación de "Perfiles Lookalike" en la Fase 1 B2C y cómo aseguramos que **los fundadores y la plataforma nunca tengan acceso a las redes de contactos de los usuarios**.

---

## 1. Fase 1 B2C: Sugerencia de Perfiles "Lookalike" (Espejo)

Dado que en la Fase 1 el comercial opera en un silo 100% privado en su computadora, la inteligencia artificial (IA local) le ayuda a clonar sus éxitos analizando sus propios datos:

*   **¿Qué es un Lookalike relacional?** Si el vendedor logró agendar una llamada con Armando Herrera (CEO de Nu México) usando un pitch específico, el sistema escanea **su propia lista de contactos locales** en IndexedDB para identificar perfiles similares:
    > *“Éxito Detectado: Tuviste una interacción exitosa con Armando Herrera (C-Level, Fintech, México). Encontré 3 perfiles espejo en tu red local que comparten la misma jerarquía e industria y con los que tienes una temperatura de relación verde/amarilla: Santiago Rodríguez (TipTop Pay) y Fernanda Ramírez (Truora). Te sugerimos atacarlos hoy con la misma plantilla.”*
*   **Privacidad:** Esta recomendación se calcula en el cliente (navegador) o de forma encriptada. No requiere compartir datos con externos.

---

## 2. El Pilar Ético: Por qué NO debemos ver los datos de los usuarios

Para ganar la confianza de comerciales independientes y cumplir con auditorías corporativas estrictas, **la plataforma opera bajo un modelo de Cero-Conocimiento (Zero-Knowledge)**. Ni Antonio, ni José, ni Juan, ni los servidores centrales de la startup pueden leer los contactos, correos o mensajes de los usuarios.

Esto nos blinda de:
1.  **Responsabilidad legal (Liability):** Si sufrimos un hackeo, los atacantes no encontrarán bases de datos de contactos de clientes porque **no las almacenamos**.
2.  **Rechazo del comercial:** El vendedor comparte sus ZIPs sabiendo que su red es 100% de su propiedad y que nadie (ni su jefe ni nosotros) la está espiando.

---

## 3. Arquitectura Criptográfica para José y Juan (E2EE & Hashing)

Para cruzar coincidencias sin ver la información en texto plano, implementamos un pipeline de encriptación de extremo a extremo (E2EE):

```
[ Navegador del Vendedor (Local) ] ──► Genera Hash SHA-256 de los dominios ──► [ Servidor de Coincidencias (Nube) ]
  - Lee: "armando@nu.com.mx"             - hash('nu.com.mx')                     - Solo compara hashes anónimos
  - Genera: hash('nu.com.mx')            - Rol: "CEO"                            - Si hay match, avisa al navegador
                                                                                   del conector para desencriptar local
```

### Paso 1: Anonimización en el Cliente (Hashing local)
Antes de enviar cualquier dato al servidor para buscar coincidencias con el CRM de la empresa (Fase 2) o círculos P2P (Fase 3), el navegador del usuario transforma los datos sensibles en Hashes criptográficos de una sola vía (**SHA-256**):
*   El correo `armando@nu.com.mx` se convierte localmente en `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
*   El dominio de la empresa se encripta.
*   El servidor central **solo recibe los hashes anónimos y la jerarquía** (ej. "CEO").

### Paso 2: Cruce de Hashes a Ciegas
El servidor compara los hashes de la base de datos de la empresa con los hashes de las redes de los vendedores. 
*   Si hay una coincidencia de hashes: El servidor sabe que *Vendedor A* tiene una conexión en la cuenta de la empresa, pero **el servidor no sabe el nombre del contacto ni su correo**.
*   Solo envía una notificación cifrada al navegador del *Vendedor A*. El navegador del vendedor recibe la alerta y descifra el nombre real de forma local en su pantalla utilizando su clave privada guardada en su sesión.
