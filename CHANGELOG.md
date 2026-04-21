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
