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
