
import abc
import datetime
from typing import TypeVar, Generic, List, Optional
from price_manager.entities.entities import (
  EntidadBase, Categoria, Proveedor, Moneda,
  TipoCotizacion, Precio, Producto, Stock, CotizacionDolar
)

T = TypeVar('T', bound=EntidadBase)

class IRepositorio(abc.ABC, Generic[T]):
  @abc.abstractmethod
  def crear(self, entidad: T) -> T: pass
  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]: pass
  @abc.abstractmethod
  def leer_todos(self) -> List[T]: pass
  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T: pass
  @abc.abstractmethod
  def eliminar(self, id: int) -> bool: pass

class IRepositorioStock(abc.ABC):
  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock: pass
  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional[Stock]: pass
  @abc.abstractmethod
  def actualizar(self, stock: Stock) -> Stock: pass
  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool: pass

class IRepositorioCotizacionDolar(abc.ABC):
  @abc.abstractmethod
  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar: pass
  @abc.abstractmethod
  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]: pass
  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]: pass
  @abc.abstractmethod
  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar: pass
  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool: pass

# --- Implementaciones Concretas ---

class RepositorioGenerico(IRepositorio[T]):
  def __init__(self):
    self._datos: dict[int, T] = {}

  def crear(self, entidad: T) -> T:
    if entidad.id in self._datos:
      raise ValueError(f"Ya existe un registro con ID {entidad.id}")
    self._datos[entidad.id] = entidad
    return entidad

  def leer_por_id(self, id: int) -> Optional[T]:
    return self._datos.get(id)

  def leer_todos(self) -> List[T]:
    return list(self._datos.values())

  def actualizar(self, entidad: T) -> T:
    if not hasattr(entidad, 'id') or entidad.id not in self._datos:
      raise ValueError("No se encontró el registro para actualizar")
    self._datos[entidad.id] = entidad
    return entidad

  def eliminar(self, id: int) -> bool:
    if id in self._datos:
      del self._datos[id]
      return True
    raise ValueError("No se encontró el registro para eliminar")

class RepositorioCategoria(RepositorioGenerico[Categoria]): pass
class RepositorioProveedor(RepositorioGenerico[Proveedor]): pass
class RepositorioMoneda(RepositorioGenerico[Moneda]): pass
class RepositorioTipoCotizacion(RepositorioGenerico[TipoCotizacion]): pass
class RepositorioProducto(RepositorioGenerico[Producto]): pass

class RepositorioStock(IRepositorioStock):
  def __init__(self):
    self._datos: dict[int, Stock] = {}

  def crear(self, stock: Stock) -> Stock:
    if stock.producto_id in self._datos:
      raise ValueError("Ya existe un registro de stock para el mismo producto.")
    self._datos[stock.producto_id] = stock
    return stock

  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
    return self._datos.get(producto_id)

  def actualizar(self, stock: Stock) -> Stock:
    if stock.producto_id not in self._datos:
      raise ValueError("No se encontró el stock para actualizar.")
    self._datos[stock.producto_id] = stock
    return stock

  def eliminar(self, producto_id: int) -> bool:
    if producto_id in self._datos:
      del self._datos[producto_id]
      return True
    return False

class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  def __init__(self):
    self._datos: List[CotizacionDolar] = []

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    if self.leer_por_tipo_y_fecha(cotizacion.tipo.id, cotizacion.fecha):
      raise ValueError("Ya existe una cotización para el mismo tipo y fecha.")
    self._datos.append(cotizacion)
    return cotizacion

  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional[CotizacionDolar]:
    for c in self._datos:
      if c.tipo.id == tipo_id and c.fecha == fecha:
        return c
    return None

  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    return sorted([c for c in self._datos if c.tipo.id == tipo_id], key=lambda x: x.fecha)

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    for i, c in enumerate(self._datos):
      if c.tipo.id == cotizacion.tipo.id and c.fecha == cotizacion.fecha:
        self._datos[i] = cotizacion
        return cotizacion
    raise ValueError("No se encontró la cotización para actualizar.")

  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    for i, c in enumerate(self._datos):
      if c.tipo.id == tipo_id and c.fecha == fecha:
        del self._datos[i]
        return True
    return False
