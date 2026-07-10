# Arquitectura de Servidores y Soberanía de Datos

Este documento técnico detalla la estrategia de infraestructura para mantener la neutralidad geopolítica y el cumplimiento estricto de privacidad (anti-FISA/anti-CLOUD Act) sin depender de los gigantes de nube estadounidenses (AWS, GCP, Azure).

---

## 1. Fase 1: Arquitectura "Serverless" y Procesamiento Local (Edge / Client-Side)

Para el MVP y la Fase 1 B2C, **el servidor de base de datos no existe**. 
*   **Procesamiento:** El parseo de los archivos ZIP/CSV se ejecuta al 100% en la memoria RAM del navegador del comercial.
*   **Almacenamiento:** Los contactos se guardan localmente en la base de datos interna del navegador (**IndexedDB**). Ningún dato de contactos viaja a la nube.
*   **Alojamiento del Código:** El archivo estático (HTML/JS) se puede hospedar en redes de distribución de contenido (CDNs) neutrales de alta seguridad (ej. **Cloudflare**, con políticas de privacidad alineadas a la UE). Dado que el servidor solo distribuye código estático y no almacena datos de usuarios, el proveedor de hosting estático es irrelevante para el cumplimiento de privacidad.

---

## 2. Fase 2 y 3: Proveedores de Nube Soberana (Sovereign Cloud)

Cuando el producto escale a bases de datos compartidas para empresas (B2B) o círculos P2P, **evitaremos a AWS, Google Cloud y Microsoft Azure** para proteger los datos de la jurisdicción del CLOUD Act de EE.UU. 

Utilizaremos infraestructura de **Nube Soberana Europea y Local**:

### 🇪🇺 Opción A: OVHcloud o Scaleway (Francia / Europa)
*   **Quiénes son:** Los proveedores de nube más grandes de Europa.
*   **Ventaja:** Son empresas de capital 100% europeo, reguladas bajo el GDPR y con datacenters en Europa. Están completamente fuera del alcance del CLOUD Act y FISA de EE.UU. Es la opción preferida por empresas europeas y globales que desconfían de la tecnología de EE.UU.

### 🇨🇭 Opción B: Infomaniak (Suiza)
*   **Quiénes son:** El gigante del hosting suizo.
*   **Ventaja:** Hospedado en Suiza, fuera de la Unión Europea y de EE.UU. Sujeto a las leyes de privacidad suizas, que son las más estrictas y neutrales del planeta.

### 🇲🇽 Opción C: KIO Networks (México)
*   **Quiénes son:** La empresa de datacenters e infraestructura tecnológica líder en México.
*   **Ventaja:** Los datos de las empresas latinoamericanas se quedan físicamente en territorio mexicano, cumpliendo con la soberanía de datos local sin intervención de nubes extranjeras.

---

## 🔒 Resumen del Stack de Privacidad para Juan y José

Para defender técnicamente la infraestructura ante Juan (Data Engineer):

1.  **Client-Side First:** Los datos sensibles del usuario se procesan y encriptan localmente.
2.  **Sovereign Cloud:** Las bases de datos relacionales y de hashes se hospedan en **OVHcloud** (datacenters en Alemania/Francia) o **KIO Networks** (México).
3.  **Zero-Knowledge Storage:** Encriptación de base de datos usando claves derivadas del cliente (el servidor solo almacena hashes ilegibles).
