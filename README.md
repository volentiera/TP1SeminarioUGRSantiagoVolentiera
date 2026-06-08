# Price Manager

## Sprint actual
**Sprint 3** — Web Scraping y comparación de precios con la competencia.

## Grupo
- **Grupo nro:** 13
- **Integrante:** Santiago Volentiera
- **Repositorio:** https://github.com/volentiera/price_manager

## Objetivo
Aplicar los conocimientos de programación orientada a objetos y
persistencia de datos en base de datos relacional, incorporando la
obtención de datos desde la web (scraping) para comparar los precios
internos con los de la competencia (Star Computación) y generar alertas
y reportes que faciliten la toma de decisiones comerciales.

## Introducción y contexto
Una empresa distribuidora de productos electrónicos necesita modernizar
su sistema de gestión de inventarios y competir con los precios del
mercado. En este tercer sprint se obtienen los precios de la competencia
mediante scraping, se comparan con los precios internos almacenados en
la base de datos relacional, y se generan alertas (CSV) y reportes
(Excel) para la toma de decisiones. El sistema registra además una
auditoría de cada operación crítica realizada.

El trabajo se basa en lo construido en los sprints anteriores:
- **Sprint 1:** modelado de dominio con POO, persistencia en archivos CSV.
- **Sprint 2:** migración a base de datos relacional con SQLAlchemy y
  consumo de API externa (DolarAPI).
- **Sprint 3:** scraping de la competencia con Scrapy y generación de
  alertas y reportes comparativos.

## Funcionalidades principales
- Gestión de inventario y stock.
- CRUD de categorías, proveedores, monedas y tipos de cotización.
- Cotización del dólar en tiempo real (DolarAPI).
- Reporte bimonetario (ARS/USD) y exportación a CSV.
- Scraping de precios de la competencia con Scrapy (spider, items,
  loaders y pipelines).
- Generación de alertas CSV por diferencia de precios mayor a un umbral.
- Reporte Excel comparativo entre precio interno y precio web.
- Auditoría persistente de las operaciones del sistema.

## Estructura del proyecto

- `database/` — conexión SQLAlchemy.
- `entities/` — entidades del dominio con encapsulamiento.
- `models/` — definición de tablas SQL.
- `migrations/` — datos semilla (CSV y SQL) y scripts de migración.
- `preload_data/` — carga inicial de datos desde CSV / SQL.
- `repositories/` — capa de persistencia (CRUD contra la DB).
- `services/` — lógica de negocio.
  - `services.py`
  - `alertas.py`
  - `reporte_excel.py`
  - `auditoria.py`
- `scraper/` — Scrapy: items, pipelines, settings, spider.
  - `spiders/star_computacion.py`
- `ui/console.py` — interfaz CLI.
- `main.py` — punto de entrada.

## Notas técnicas
- **Scraping con Scrapy:** el spider `StarComputacionSpider` navega por
  las categorías reales del sitio mediante un `CATEGORIA_MAP` y
  estructura los datos extraídos con Loaders e Items.
- **Rate limiting:** se configura `DOWNLOAD_DELAY = 2`,
  `CONCURRENT_REQUESTS = 1` y `RANDOMIZE_DOWNLOAD_DELAY = True` para
  evitar bloqueos por IP al consumir el sitio.

## Cómo ejecutar
1. Ejecutar el notebook `03_Price_Manager_Grupo_13.ipynb` desde Colab.
2. Las dependencias se instalan automáticamente en la primera celda.
3. La función `main(import_default_data=True)` precarga los datos en la
   base si la misma se encuentra vacía y arranca el menú interactivo.
