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
