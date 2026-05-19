import datetime

class EntidadBase:
    """Clase base para que funcione el TypeVar en los repositorios genéricos."""
    pass

class Categoria(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

class Proveedor(EntidadBase):
    def __init__(self, id: int, nombre: str, contacto: str):
        self.id = id
        self.nombre = nombre
        self.contacto = contacto

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @property
    def contacto(self) -> str:
        return self._contacto

    @contacto.setter
    def contacto(self, value: str):
        self._contacto = value

class Moneda(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

class Precio(EntidadBase):
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

    @property
    def moneda(self) -> Moneda:
        return self._moneda

    @moneda.setter
    def moneda(self, value: Moneda):
        self._moneda = value

    @property
    def fecha(self) -> datetime.date:
        return self._fecha

    @fecha.setter
    def fecha(self, value: datetime.date):
        self._fecha = value

class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

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

    @property
    def fecha(self) -> datetime.date:
        return self._fecha

    @fecha.setter
    def fecha(self, value: datetime.date):
        self._fecha = value

    @property
    def tipo(self) -> TipoCotizacion:
        return self._tipo

    @tipo.setter
    def tipo(self, value: TipoCotizacion):
        self._tipo = value

class Producto(EntidadBase):
    def __init__(self, id: int, nombre: str, descripcion: str, precio: Precio,
                 categoria: Categoria, proveedor: Proveedor):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.proveedor = proveedor

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str):
        self._descripcion = value

    @property
    def precio(self) -> Precio:
        return self._precio

    @precio.setter
    def precio(self, value: Precio):
        self._precio = value

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @categoria.setter
    def categoria(self, value: Categoria):
        self._categoria = value

    @property
    def proveedor(self) -> Proveedor:
        return self._proveedor

    @proveedor.setter
    def proveedor(self, value: Proveedor):
        self._proveedor = value

class Stock(EntidadBase):
    def __init__(self, producto_id: int, cantidad: int = 0):
        self.producto_id = producto_id
        self.cantidad = cantidad

    @property
    def producto_id(self) -> int:
        return self._producto_id

    @producto_id.setter
    def producto_id(self, value: int):
        self._producto_id = value

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        if nueva_cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._cantidad = nueva_cantidad
