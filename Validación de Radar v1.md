# Validación de Radar v1

## Pruebas ejecutadas

- `node test_radar_core.js`: correcto; las pruebas de búsqueda por tema, año, dirección y fallback curado pasaron.
- `node --check radar_core.js`: correcto; no hay errores de sintaxis en el núcleo nuevo.
- Dashboard local: carga y `window.RadarCore` está disponible con versión `0.1.0`.

## Observaciones del navegador local

- Al abrir `index.html` directamente con `file://`, el `fetch` de `master_data.js` produce un warning porque los navegadores bloquean fetch local. El fallback existente carga el script y el dashboard termina funcionando.
- La bóveda demo `vault_antonio` se guarda localmente con 3,039 contactos.
- La consola muestra un error independiente y preexistente: Supabase no encuentra `public.connections` en el schema cache. Esto confirma que el esquema documentado y el proyecto Supabase conectado no están alineados todavía.
- La integración de `radar_core.js` no produjo errores de carga.

## Interpretación

La primera entrega es compatible con el prototipo curado y no sustituye todavía el login, Supabase, la persistencia de mensajes ni el modelo de snapshots. El siguiente trabajo debe escoger un único modelo Supabase antes de activar carga multiusuario.

Fecha: 2026-08-23

## Validación visual adicional

- El dashboard local mantiene el dataset curado de 3,039 contactos.
- La sección Mi Perfil muestra el selector `Contexto profesional seleccionado / ICP manual / Campaña histórica`.
- Se muestran los contextos profesionales Clip, Fiserv, LATAM Commerce, ENFA Delivery, JTI y Conagra Brands.
- El selector manual todavía requiere interacción para mostrar el formulario; la estructura quedó añadida al HTML y el núcleo de scoring quedó conectado al modo manual.

## Prueba del ICP manual

El modo `ICP manual` se activa desde el selector de Mi Perfil y muestra siete campos: nombre, industrias, países, cargos objetivo, empresas o dominios, palabras clave y exclusiones. La prueba local aceptó un perfil de pagos y fintech en México con cargos objetivo y palabras clave. El panel recalculó la navegación y dejó los resultados en cero porque el dataset curado no tiene un contexto suficientemente coincidente con todos los campos; esto es un comportamiento esperable del score inicial y deberá mostrar desglose y explicación en la siguiente iteración.
