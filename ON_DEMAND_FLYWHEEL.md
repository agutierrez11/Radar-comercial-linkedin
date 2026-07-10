# Arquitectura de Datos On-Demand: El Círculo Virtuoso (Flywheel) de NERV

Este documento técnico describe el diseño de la base de datos y la estrategia de acumulación de datos de **Radar Comercial + NERV OS**. Explica cómo pasamos de un modelo costoso de bases de datos masivas pre-escrapeadas a un modelo de enriquecimiento bajo demanda financiado por los propios usuarios.

---

## 1. El Problema del Modelo Tradicional (Apollo / ZoomInfo)

Las plataformas de prospección clásicas intentan almacenar "todo el universo" de empresas y contactos del planeta. Esto genera tres problemas gigantescos para una startup:
1.  **Costos de Almacenamiento Masivos:** Terabytes de datos que requieren servidores costosos.
2.  **Caducidad de Datos (Data Decay):** Los datos cambian constantemente (personas cambian de puesto, empresas cierran) haciendo que la base de datos se vuelva obsoleta en meses si no se actualiza continuamente con scraping masivo.
3.  **Bajo ROI inicial:** Invertir miles de dólares en raspar bases de datos que quizás ningún cliente consultará jamás.

---

## 2. La Solución: Enriquecimiento On-Demand (Bajo Demanda)

En lugar de almacenar todo el universo de antemano, **empezamos con una base de datos vacía** y la enriquecemos en tiempo real únicamente cuando el usuario lo solicita.

```
[ Usuario solicita análisis de "Empresa X" ] ──► ¿Existe en la caché global?
                                                           │
                              ┌────────────────────────────┴────────────────────────────┐
                              ▼ SI                                                      ▼ NO
                 [ Retorna metadata curada ]                               [ NERV escrapea y cura "Empresa X" ]
                                                                                        │
                                                                                        ▼
                                                                           [ Guarda en la base global ]
                                                                                        │
                                                                                        ▼
                                                                           [ Cobra crédito al usuario ]
```

1.  **Gatillo del Usuario:** El comercial sube su `Connections.csv` y hace clic en *"Investigar"* para un lead de la "Empresa X".
2.  **Consulta de Caché:** El backend revisa si ya tenemos la metadata curada de la "Empresa X" en nuestra base de datos global.
3.  **Enriquecimiento en Caliente (On-Demand):**
    *   Si **NO** existe, el motor NERV se activa, realiza OSINT, escrapea la web pública de la empresa, analiza tecnologías utilizadas, vertical e información relevante, y genera la metadata limpia.
    *   Si **SÍ** existe, entrega los datos directamente de la caché local (ahorrando tiempo y tokens de API).
4.  **Cobre por Enriquecimiento:** Se descuenta un crédito al usuario (ej. 1 crédito de su plan mensual de $10 USD) por realizar el enriquecimiento inicial.

---

## 3. El Volante de Inercia de Datos (The Data Flywheel)

Dado que la información corporativa de las empresas (sector, tamaño, tecnologías, noticias) es **información pública**, el sistema opera bajo un círculo virtuoso:

*   **Financiado por el Cliente:** El comercial paga la suscripción o los créditos para enriquecer sus leads de interés. El cliente financia el costo de la API y el scraping.
*   **Enriquecimiento Acumulativo de NERV:** Toda la metadata de la "Empresa X" curada por NERV se almacena de forma permanente en nuestra base de datos central de conocimiento.
*   **Efecto Red de Datos:** Con el tiempo, a medida que miles de comerciales individuales enriquecen a sus clientes objetivo, **nuestra base de datos corporativa de NERV crece y se actualiza de forma orgánica, gratuita y automática**. 
*   **Margen de Utilidad Creciente:** El primer usuario en consultar "Empresa X" nos cuesta tokens de scraping. El segundo, tercer y cuarto usuario que consulten la misma empresa nos cuestan **cero pesos**, incrementando nuestro margen de ganancia a casi el 100% sobre esas consultas.
