---
name: crawl4ai-web-enrichment
description: Scraping y crawling web ultrarrápido nativo para LLMs (basado en unclecode/crawl4ai). Extracción de metadata de cuentas objetivo, tecnologías activas, eventos disparadores (trigger events) y actualización de perfiles corporativos sin bloqueos.
---

# Crawl4AI Web Enrichment Skill — Enriquecimiento Web Agéntico a Cero Costo

Esta habilidad habilita la capacidad de extraer, analizar y estructurar automáticamente el contenido de las webs de empresas y perfiles corporativos objetivo utilizando crawlers ultrarrápidos y nativos para modelos de lenguaje (**Crawl4AI**).

---

## 🎯 Caso de Uso (Modelo BYOK & Costo Cero)

Para validar cuentas objetivo sin pagar APIs costosas por cada solicitud (tipo Apollo/Lusha), esta habilidad permite:
- Extraer el stack de tecnologías de pago de la web de un comercio (ej. si usan Stripe, Adyen, Mercado Pago, clip, Shopify, WooCommerce).
- Detectar noticias recientes, rondas de financiamiento, aperturas de vacantes y anuncios corporativos (*Trigger Events*).
- Formatear el contenido extraído a Markdown limpio optimizado para el consumo de modelos como Gemini 2.5 Flash, GPT-4o mini o Qwen 2.5.

---

## 🛠️ Arquitectura de Extracción con Crawl4AI

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def enrich_target_account(company_url: str):
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=10,
        exclude_external_links=True,
        remove_overlay_elements=True
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=company_url, config=config)
        if result.success:
            markdown_content = result.markdown
            print(f"[+] Scraping exitoso para {company_url}. Longitud: {len(markdown_content)} caracteres.")
            return markdown_content
        else:
            print(f"[-] Error al raspar {company_url}: {result.error_message}")
            return None
```

---

## 🔍 Reglas de Extracción y Estructuración

1. **Format-First:** Toda información extraída debe convertirse a Markdown semántico con encabezados claros (`#`, `##`) para minimizar el uso de tokens.
2. **Filtrado de Basura:** Eliminar automáticamente avisos de cookies, footers de navegación irrelevantes y scripts de rastreo para enviar únicamente contenido de alto valor al LLM.
3. **Trigger Event Detection Prompt:**
   ```text
   Analiza el siguiente texto en Markdown extraído de la web de [Empresa]:
   1. Identifica los procesadores de pago, gateways o ERPs mencionados o visibles en el checkout.
   2. Extrae cualquier anuncio reciente de expansión, financiamiento o nuevas alianzas en los últimos 6 meses.
   3. Determina el nivel de prioridad comercial (Alta, Media, Baja) para un pitch de pasarelas de pago B2B.
   ```
