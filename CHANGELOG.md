## [Ejercicio 07] - 2026-06-12

### Añadido
- Incorporación de opciones 7, 8 y 9 al menú principal en `console.py`.
- Opción 7: Ejecutar scraping y generar alertas CSV.
- Opción 8: Generar reporte Excel de competencia.
- Opción 9: Ver historial de auditoría.
- Descarga automática de archivos generados al salir con opción 0.

## [Ejercicio 06] - 2026-06-11

### Añadido
- Implementación del decorador `@auditar` en `auditoria.py`.
- Creación automática de la tabla `auditoria` en la base de datos.
- Registro de acción, fecha y resultado de cada operación auditada.
- Implementación de `obtener_historial_auditoria()` para consulta de registros.
- Aplicación del decorador en `_menu_scraping_alertas()` y `_menu_reporte_excel()`.

## [Ejercicio 05] - 2026-06-10

### Añadido
- Implementación de `generar_reporte_excel()` en `reporte_excel.py`.
- Reporte con columnas: Producto, Precio interno, Precio web, Diferencia, Fecha de extracción.
- Uso de `pandas` para generar el archivo `.xlsx`.

## [Ejercicio 04] - 2026-06-09

### Añadido
- Implementación de `generar_alertas_csv()` en `alertas.py`.
- Comparación de precio interno (DB) vs precio web (JSON del scraper).
- Generación de archivo CSV con alertas para diferencias superiores al umbral ingresado por el usuario.

## [Ejercicio 03] - 2026-06-08

### Añadido
- Implementación de `StarComputacionSpider` con Scrapy navegando por categorías reales del sitio.
- Creación de `items.py` con `ProductoWebItem` usando Loaders, `MapCompose` y `TakeFirst`.
- Creación de `pipelines.py` con `PriceManagerPipeline` para limpiar precios y normalizar URLs.
- Creación de `settings.py` con configuración de Scrapy.
- Implementación de `run_scraper.py` con `CrawlerProcess` que ejecuta el spider real de Scrapy.
- Integración de `scrapy-impersonate` para sortear el filtrado TLS (WAF) que devolvía 403 a las requests del cliente Scrapy por defecto.
- Mapeo de productos internos a categorías reales de Star Computación via `CATEGORIA_MAP`.

## [Ejercicio 02] - 2026-06-07

### Añadido
- Implementación de `cargar_datos_sql()` en `preload_data.py`.
- Función que lee un archivo `.sql` y ejecuta sus sentencias usando `ConexionDB`.

## [Ejercicio 01] - 2026-06-06

### Añadido
- Creación y cambio a la rama `Sprint_3` desde `Sprint_2`.

# Changelog

## [2026-04-21]

### Añadido

#### Módulo de Entidades (price_manager/entities/entities.py)
- Creación del archivo de entidades base.
- Implementación de la clase EntidadBase para soporte de tipado en repositorios genéricos.
- Definición de las entidades principales del dominio: Categoria, Proveedor, Moneda, TipoCotizacion y Producto.
- Implementación de la clase Precio con validación mediante properties para evitar valores negativos.
- Implementación de la clase CotizacionDolar con validación para asegurar valores estrictamente positivos.
- Implementación de la clase Stock con validación para impedir cantidades de inventario negativas.

## [2026-04-22]

### Añadido

#### Módulo de Repositorios (price_manager/repositories/repositories.py)
- Creación del archivo de persistencia en memoria.
- Definición de interfaces abstractas (IRepositorio, IRepositorioStock, IRepositorioCotizacionDolar) utilizando abc para establecer los contratos de operaciones CRUD.
- Implementación de la clase RepositorioGenerico para el manejo de las entidades estándar.
- Implementación de la clase RepositorioStock con operaciones específicas basadas en producto_id.
- Implementación de la clase RepositorioCotizacionDolar con almacenamiento en listas y métodos específicos para búsquedas por tipo y fecha.
- Incorporación de validaciones para evitar duplicados y control de existencia de registros (manejo de errores con ValueError).

## [2026-04-23]

### Añadido

#### Módulo de Servicios (price_manager/services/services.py)
- Creación del archivo de la capa de servicios (lógica de negocio).
- Implementación de `ServicioGenerico` para centralizar operaciones CRUD básicas y manejo de errores de entidades no encontradas.
- Definición de servicios específicos para `Categoria`, `Proveedor`, `Moneda` y `TipoCotizacion`.
- Implementación de `ServicioProducto` con soporte para dependencias de categorías y proveedores.
- Desarrollo de `ServicioStock` con lógica para el registro de movimientos (entradas/salidas) y validación de stock inicial no negativo.
- Desarrollo de `ServicioCotizacionDolar` para la gestión de registros históricos y validación de tipos de cotización existentes.
- Aplicación de inyección de dependencias para desacoplar la lógica de negocio de los repositorios.

## [2026-04-24]

### Añadido

#### Módulos de Migraciones y Precarga de Datos (`price_manager/migrations/` y `price_manager/preload_data/preload_data.py`)
- Creación de script de migraciones para generar archivos CSV con datos semilla (hardware y componentes de PC).
- Creación automática del directorio de almacenamiento `price_manager/migrations/csv`.
- Generación de 10 registros iniciales para las entidades: `categorias`, `proveedores`, `monedas`, `tipos_cotizacion` y `productos`.
- Creación del archivo `preload_data.py` para la lectura e hidratación de datos.
- Implementación de la función `leer_csv` para parsear los archivos utilizando `csv.DictReader`.
- Implementación de la función `cargar_datos` para instanciar las entidades del dominio (incluyendo la composición de `Precio`) a partir de los diccionarios leídos.
- Integración de la precarga con la capa de servicios, incluyendo el manejo de excepciones `ValueError` para omitir silenciosamente la inserción de registros duplicados.

## [2026-04-25]

### Añadido
#### Módulo de Interfaz de Usuario (`price_manager/ui/console.py`)
- Creación de la clase `InterfazConsola` para la interacción por línea de comandos (CLI).
- Implementación de un menú principal persistente con navegación por opciones numéricas.
- Desarrollo de sub-menús para la visualización de productos (incluyendo precios y monedas) y gestión de maestros (categorías y proveedores).
- Implementación de un sistema interactivo de ajuste de stock con entrada de datos y validación de errores en tiempo real.
- Integración de consultas de históricos de cotización de divisas.
- Inyección de la capa de servicios en la UI para garantizar la separación de responsabilidades entre la visualización y la lógica de negocio.

## [2026-04-26]

### Añadido

#### Archivo Principal y Punto de Entrada (`price_manager/main.py`)
- Creación del script principal de orquestación e inicialización del sistema.
- Implementación de la función `main` para instanciar y conectar las distintas capas de la arquitectura.
- Instanciación centralizada de la capa de persistencia en memoria (Repositorios).
- Instanciación de la capa de lógica de negocio (Servicios) aplicando inyección de dependencias manual.
- Integración condicional de la función de precarga de datos CSV (`import_default_data`).
- Inicialización y arranque del bucle principal de la interfaz de consola (`InterfazConsola`).
- Configuración del bloque de ejecución estándar `if __name__ == "__main__":`.

## [2026-05-19]

### Añadido
#### Inicialización Sprint 2 (Ejercicio 01)
- Creación y cambio a la rama `Sprint_2`.
- Creación de la estructura de directorios para la base de datos relacional (`database`, `models`, `migrations/sql`).
- Creación de archivos base vacíos (`connection.py`, `models.py`, `migrations.py`).

## [2026-05-21]

### Añadido
#### Conexión a Base de Datos (Ejercicio 02)
- Creación del archivo `price_manager/database/connection.py`.
- Implementación de la clase `ConexionDB` utilizando `SQLAlchemy` con motor SQLite.
- Configuración para la creación automática del directorio de la base de datos local (`/content/base_de_datos/`).

## [2026-05-21]

### Añadido
#### Manejo de Transacciones (Ejercicio 03)
- Actualización del archivo `price_manager/database/connection.py`.
- Implementación de un *context manager* (`transaccion`) en la clase `ConexionDB`.
- Incorporación de lógica de transacciones seguras con `commit` automático y `rollback` en caso de excepciones.

## [2026-05-22]

### Añadido
#### Creación de Tablas y Relaciones (Ejercicio 04)
- Creación del archivo `price_manager/models/models.py`.
- Implementación de la función `crear_tablas` utilizando sentencias SQL crudas (raw SQL).
- Definición de la estructura de la base de datos y tipos para: `categorias`, `proveedores`, `monedas`, `tipos_cotizacion`, `productos`, `stock` y `cotizaciones_dolar`.
- Establecimiento de relaciones (Foreign Keys) e integridad referencial.
- Uso del *context manager* transaccional para ejecución segura (rollback automático en caso de fallo).

## [2026-05-23]

### Añadido
#### Migración de Datos (Ejercicio 05)
- Creación del archivo `price_manager/migrations/migrations.py`.
- Implementación de la función `migrar_datos` para leer los datos semilla desde archivos CSV.
- Generación automática de archivos `.sql` con sentencias de inserción (`INSERT OR IGNORE`).
- Ejecución de las sentencias SQL en la base de datos utilizando el *context manager* de transacciones seguras.

## [2026-05-24]

### Modificado
#### Capa de Persistencia a Base de Datos (Ejercicio 06)
- Refactorización completa del archivo `price_manager/repositories/repositories.py`.
- Reemplazo del almacenamiento en memoria (diccionarios y listas) por conexión directa a la base de datos SQLite.
- Implementación de operaciones CRUD (Create, Read, Update, Delete) para todas las entidades utilizando SQL crudo y la función `text` de SQLAlchemy.
- Integración del *context manager* transaccional (`self.db.transaccion()`) en cada operación de repositorio para asegurar atomicidad y consistencia.
- Hidratación automática de entidades vinculadas (composición de objetos) al leer desde la base de datos (Ej. instanciar `Moneda`, `Categoria` y `Proveedor` al leer un `Producto`).

## [2026-05-25]

### Añadido
#### Integración de API y Variables de Entorno (Ejercicio 07)
- Creación del archivo `.env` para almacenar la configuración de `API_URL` de forma segura.
- Actualización de la capa de servicios (`price_manager/services/services.py`).
- Implementación de la librería `python-dotenv` para la carga de variables de entorno.
- Incorporación de la función `obtener_cotizaciones` dentro de `ServicioCotizacionDolar` para consumir la API externa (`dolarapi.com`).
- Lógica de mapeo y registro automático de cotizaciones JSON a la base de datos relacional cruzando con los tipos existentes.

## [2026-05-26]

### Añadido
#### Reportes, Listas Bimonetarias y Exportación (Ejercicio 08)
- Modificación del menú principal en `price_manager/ui/console.py` para incluir la sección "Reportes y Exportación".
- Integración de opción interactiva para gatillar la descarga de cotizaciones desde la API.
- Implementación de lógica de conversión bimonetaria en tiempo real (ARS/USD) según la cotización histórica más reciente de la base de datos.
- Desarrollo de la función de exportación a CSV iterando sobre todos los productos y calculando equivalencias cruzadas contra todos los tipos de dólar registrados.

## [2026-06-06]

### Añadido
#### Inicialización Sprint 3 (Ejercicio 01)
- Creación y cambio a la rama `Sprint_3` desde `Sprint_2`.

## [2026-06-07]

### Añadido
#### Carga de datos SQL (Ejercicio 02)
- Implementación de `cargar_datos_sql()` en `preload_data.py`.
- Función que lee un archivo `.sql` y ejecuta sus sentencias usando `ConexionDB`.

## [2026-06-08]

### Añadido
#### Scraper de Star Computación (Ejercicio 03)
- Implementación de `StarComputacionSpider` con Scrapy navegando por categorías reales del sitio.
- Creación de `items.py` con `ProductoWebItem` usando Loaders, `MapCompose` y `TakeFirst`.
- Creación de `pipelines.py` con `PriceManagerPipeline` para limpiar precios y normalizar URLs.
- Creación de `settings.py` con configuración de Scrapy.
- Implementación de `run_scraper.py` con `requests` y `BeautifulSoup` como solución funcional en Colab.
- Mapeo de productos internos a categorías reales de Star Computación via `CATEGORIA_MAP`.

## [2026-06-09]

### Añadido
#### Alertas de precios (Ejercicio 04)
- Implementación de `generar_alertas_csv()` en `alertas.py`.
- Comparación de precio interno (DB) vs precio web (JSON del scraper).
- Generación de archivo CSV con alertas para diferencias superiores al umbral ingresado por el usuario.

## [2026-06-10]

### Añadido
#### Reporte Excel (Ejercicio 05)
- Implementación de `generar_reporte_excel()` en `reporte_excel.py`.
- Reporte con columnas: Producto, Precio interno, Precio web, Diferencia, Fecha de extracción.
- Uso de `pandas` para generar el archivo `.xlsx`.

## [2026-06-11]

### Añadido
#### Auditoría del sistema (Ejercicio 06)
- Implementación del decorador `@auditar` en `auditoria.py`.
- Creación automática de la tabla `auditoria` en la base de datos.
- Registro de acción, fecha y resultado de cada operación auditada.
- Implementación de `obtener_historial_auditoria()` para consulta de registros.
- Aplicación del decorador en `_menu_scraping_alertas()` y `_menu_reporte_excel()`.

## [2026-06-12]

### Añadido
#### Menú Sprint 3 (Ejercicio 07)
- Incorporación de opciones 7, 8 y 9 al menú principal en `console.py`.
- Opción 7: Ejecutar scraping y generar alertas CSV.
- Opción 8: Generar reporte Excel de competencia.
- Opción 9: Ver historial de auditoría.
- Descarga automática de archivos generados al salir con opción 0.
