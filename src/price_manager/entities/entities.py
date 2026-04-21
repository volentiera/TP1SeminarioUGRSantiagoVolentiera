import datetime

class EntidadBase:
    """Clase base para que funcione el TypeVar en los repositorios genéricos."""
    pass

class Categoria(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

class Proveedor(EntidadBase):
    def __init__(self, id: int, nombre: str, contacto: str):
        self.id = id
        self.nombre = nombre
        self.contacto = contacto

class Moneda(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

class Precio:
    def __init__(self, valor: float, moneda: Moneda, fecha: datetime.date):
        self.valor = valor
        self.moneda = moneda
        self.fecha = fecha

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: float):
        if nuevo_valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._valor = nuevo_valor

class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

class CotizacionDolar(EntidadBase):
    def __init__(self, valor: float, fecha: datetime.date, tipo: TipoCotizacion):
        self.valor = valor
        self.fecha = fecha
        self.tipo = tipo

    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: float):
        if nuevo_valor <= 0:
            raise ValueError("La cotización del dólar debe ser estrictamente positiva.")
        self._valor = nuevo_valor

class Producto(EntidadBase):
    def __init__(self, id: int, nombre: str, descripcion: str, precio: Precio,
                 categoria: Categoria, proveedor: Proveedor):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.proveedor = proveedor

class Stock(EntidadBase):
    def __init__(self, producto_id: int, cantidad: int = 0):
        self.producto_id = producto_id
        self.cantidad = cantidad

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        if nueva_cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._cantidad = nueva_cantidad
