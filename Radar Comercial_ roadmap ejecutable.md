# Radar Comercial: roadmap ejecutable

## Objetivo

Evolucionar el prototipo personal de Antonio hacia una herramienta local-first de inteligencia comercial, sin saturarla de fuentes ni comenzar todavía con COSMA. La primera versión debe resolver bien cuatro tareas: buscar en la red y en las conversaciones, aprender de la actividad comercial, definir el ICP con contexto histórico o manual y conservar snapshots sin perder la historia.

## Alcance confirmado

Radar Comercial es el producto propio de Antonio. El dataset curado actual sigue siendo la fuente principal de la demo. El ZIP original se conserva como fuente histórica, pero no se incorpora automáticamente al dashboard. COSMA queda pendiente como capa visual futura.

El caso real de demostración es Antonio, con la información curada de su bóveda y una muestra de conversaciones completas, especialmente la campaña de batas quirúrgicas, cubrebocas y EPP de 2020. Giovanna y el modo colectivo quedan fuera de la primera entrega funcional; no deben bloquear la estabilización del Radar personal.

## Estado actual y estado objetivo

| Área | Estado actual | Estado objetivo |
|---|---|---|
| Datos | Dataset curado y enriquecido mezclado con demo y archivos estáticos | Dataset curado como fuente activa; ZIP original como snapshot histórico separado |
| Conversaciones | Conteos, snippets y análisis preprocesado; el corpus completo se carga de forma temporal | Conversaciones completas privadas, indexadas por fecha, tema, dirección y campaña |
| Búsqueda | Búsqueda por una consulta exacta y navegación a Mi Red | Una caja de búsqueda unificada con resultados explicables y filtros progresivos |
| ICP | Contexto elegido desde Positions y override textual | Contexto profesional + ICP manual estructurado + campañas históricas |
| Empresa | Nombre y texto usados para inferir sector | Entidad empresarial con URL, dominio, país, sector, fechas y confianza |
| Purga | Marca Descartado y oculta el contacto | Conservar, archivar, revisar o borrar definitivamente con alcance explícito |
| Snapshots | No existe modelo formal | Cada ZIP se conserva con fecha, hash, fuente y comparación contra snapshots anteriores |
| Supabase | Integración parcial y modelos de tablas mezclados | Una sola arquitectura canónica, Auth real, RLS probado y Storage privado |
| COSMA | Grafo estilo demo | Pendiente; se integrará solo cuando el modelo de datos sea estable |

## Roadmap por fases

### Fase cero: proteger y fijar la línea base

Antes de modificar funcionalidad, crear una etiqueta o rama de respaldo del commit actual, retirar del repositorio los datasets que no deban ser públicos y documentar la versión curada que se usará en la demo. No se borra el ZIP original local; se separa del código.

Criterio de terminado: la versión actual puede abrirse, cargar el dataset curado, navegar por Mi Red, ICP y Mensajes, y volver a un estado anterior mediante Git.

### Fase uno: búsqueda simple y decisiones sobre datos

Agregar una única búsqueda que consulte contactos, mensajes completos si están cargados, snippets, notas, empresas y cargos. El resultado debe indicar por qué coincide y permitir `Conservar`, `Archivar`, `Revisar después` o `Eliminar definitivamente`.

No se agregan más filtros visibles. País, industria, cargo, sentimiento y fecha pasan a un panel de filtros opcionales. La consulta `batas cubrebocas 2020` debe devolver las conversaciones relacionadas con la campaña histórica cuando el corpus esté cargado.

Criterio de terminado: una búsqueda de palabras o frase devuelve resultados en menos de un segundo sobre la bóveda curada; una búsqueda sin mensajes completos no falla, sino que utiliza snippets y muestra la fuente del resultado.

### Fase dos: análisis comercial de conversaciones

Conservar la conversación completa separada del contacto. Derivar dirección, primer pitch, respuesta posterior, tema, campaña, objeción, siguiente paso y resultado. La pantalla de Mensajes debe mostrar el aprendizaje comercial, no solo sentimiento.

El primer caso de uso será la campaña EPP de 2020. El usuario podrá ver qué ofreció, qué argumentos utilizó, quién respondió y qué patrón de apertura tuvo mejor resultado.

Criterio de terminado: una conversación puede abrirse completa; sus mensajes están ordenados cronológicamente; el sistema distingue mensajes enviados por Antonio de mensajes recibidos; y puede filtrarse por campaña y año.

### Fase tres: ICP robusto y manual

Mantener el selector de posiciones históricas, pero transformarlo en un contexto profesional enriquecido. Crear ICP manual con nombre, industrias, países, cargos, palabras clave, exclusiones y pesos. Separar `contexto profesional` de `perfil ICP` y de `campaña histórica`.

Añadir desambiguación de empresas. Si el nombre tiene varias coincidencias, el usuario confirma la entidad correcta o marca la empresa como ambigua. El score muestra un desglose explicable y una confianza de identidad empresarial.

Criterio de terminado: Clip, Fiserv y LATAM Commerce se pueden seleccionar como contextos diferentes; el usuario puede crear un ICP de EPP 2020 aunque no corresponda a su cargo actual; y PayMind no se trata como una sola empresa sin confirmación.

### Fase cuatro: snapshots y evolución de la bóveda

Cada ZIP genera un snapshot inmutable. Se guarda la fuente original, una versión normalizada, una versión enriquecida y los resultados derivados. Una persona ausente del snapshot nuevo se marca como `missing_from_latest_snapshot`, no se borra automáticamente. Si reaparece, se reactiva la misma identidad y se agrega una nueva observación temporal.

Criterio de terminado: una comparación entre dos snapshots muestra contactos nuevos, ausentes, reactivados, cambios de empresa, cambios de cargo y conversaciones nuevas sin duplicar identidades.

### Fase cinco: Supabase y privacidad multiusuario

Conectar el login visible a Supabase Auth, eliminar la identidad paralela demo para producción, definir un único proyecto y aplicar RLS a todas las tablas. La bóveda del usuario debe quedar aislada por `auth.uid()`.

Para zero-knowledge estricto, los datos brutos se cifran antes de salir del navegador. Si se empieza con RLS y Storage privado, debe describirse como una versión privacy-first, no como zero-knowledge.

Criterio de terminado: dos usuarios de prueba no pueden leer ni modificar datos ajenos; el administrador no puede consultar datos brutos mediante una ruta normal del dashboard; y las políticas tienen pruebas de lectura, inserción, actualización y borrado.

### Fase seis: COSMA opcional

Cuando las fases anteriores estén estables, generar desde Radar una vista de nodos y vínculos autorizados. COSMA será únicamente la visualización. Radar seguirá siendo la fuente de verdad para permisos, scoring y datos.

## Modelo de datos mínimo

```text
vault_snapshots
- id
- owner_id
- source_hash
- source_filename
- captured_at
- processed_at
- status

contact_identities
- id
- owner_id
- identity_key
- canonical_linkedin_url
- first_seen_at
- last_seen_at

contact_versions
- id
- identity_id
- snapshot_id
- name
- company_name
- company_entity_id
- position
- country
- connected_on
- present_in_snapshot
- source
- observed_at
- confidence

conversation_threads
- id
- owner_id
- contact_identity_id
- conversation_key
- first_message_at
- last_message_at
- message_count
- campaign
- commercial_direction
- outcome

conversation_messages
- id
- thread_id
- owner_id
- message_key
- message_at
- sender_type
- content_private_or_encrypted
- first_seen_snapshot_id
- last_seen_snapshot_id

company_entities
- id
- canonical_name
- linkedin_url
- domain
- country
- industry
- confidence

icp_profiles
- id
- owner_id
- name
- mode
- industries
- countries
- target_titles
- keywords
- exclusions
- weights

vault_decisions
- id
- owner_id
- entity_type
- entity_id
- decision: keep | archive | review | delete
- decided_at
- reason
```

## Instrucciones de implementación

1. Trabajar en una rama `radar-v1-foundation`, nunca directamente sobre `main`.
2. Mantener `master_data.js` y el dataset curado como demo, pero etiquetarlos como datos de demostración.
3. Añadir el módulo `radar-core.js` de esta entrega y probarlo con datos sintéticos mínimos antes de conectarlo a `index.html`.
4. Sustituir gradualmente `handleTalkToNetworkSearch()` por `RadarCore.searchVault()`.
5. Sustituir el override textual por `icp_profiles` y conservar el selector de posiciones como contexto.
6. Cambiar la purga para que primero marque una decisión y solo ejecute borrado físico mediante una acción separada.
7. Añadir el esquema SQL de la migración antes de crear rutas de Supabase.
8. Probar dos usuarios y dos snapshots antes de cargar datos de terceros.
9. Ejecutar una revisión de datos sensibles antes de cada push.
10. Solo desplegar cuando las pruebas de no regresión y los controles de acceso estén comprobados.

## Criterios de no regresión

| Prueba | Resultado requerido |
|---|---|
| Abrir el dashboard sin ZIP completo | Carga el dataset curado y no muestra un error falso |
| Buscar un contacto por nombre | Aparece el contacto y se conserva la navegación actual |
| Buscar una palabra de una conversación | Aparece la conversación completa o se informa que solo existe un snippet |
| Cambiar Clip por Fiserv | Cambia el contexto del ICP y recalcula scores |
| Crear un ICP manual | No modifica ni elimina posiciones históricas |
| Marcar un contacto como archivado | Sale de la vista activa, pero conserva historial |
| Eliminar definitivamente | Elimina datos asociados según el alcance confirmado |
| Cargar un segundo snapshot | No duplica contactos ni sobrescribe el anterior |
| Iniciar sesión con otro usuario | No descarga la bóveda del usuario anterior |

## Decisión de alcance

La siguiente entrega no incluye COSMA, las 49 fuentes del export, un constructor Power BI completo, matching entre usuarios ni automatización de APIs de terceros. Primero debe entregar una búsqueda sencilla, una memoria comercial útil, un ICP controlable y una bóveda histórica confiable.
