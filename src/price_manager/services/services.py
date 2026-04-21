
import datetime
from typing import List, Optional, Any

from price_manager.entities.entities import Stock, CotizacionDolar

class ServicioGenerico:
  def __init__(self, repositorio: Any):
    self.repo = repositorio

  def crear(self, entidad: Any) -> Any:
    return self.repo.crear(entidad)

  def obtener(self, id: int) -> Any:
    entidad = self.repo.leer_por_id(id)
    if not entidad:
      raise ValueError(f"No se encontró la entidad con ID {id}")
    return entidad

  def listar_todos(self) -> List[Any]:
    return self.repo.leer_todos()

  def actualizar(self, entidad: Any) -> Any:
    return self.repo.actualizar(entidad)

  def eliminar(self, id: int) -> bool:
    return self.repo.eliminar(id)

class ServicioCategoria(ServicioGenerico): pass
class ServicioProveedor(ServicioGenerico): pass
class ServicioMoneda(ServicioGenerico): pass
class ServicioTipoCotizacion(ServicioGenerico): pass

class ServicioProducto(ServicioGenerico):
  def __init__(self, repo_producto: Any, srv_categoria: Any, srv_proveedor: Any):
    super().__init__(repo_producto)
    self.srv_categoria = srv_categoria
    self.srv_proveedor = srv_proveedor

class ServicioStock:
  def __init__(self, repo_stock: Any, srv_producto: Any):
    self.repo_stock = repo_stock
    self.srv_producto = srv_producto

  def registrar_movimiento(self, producto_id: int, cantidad: int) -> None:
    self.srv_producto.obtener(producto_id)
    stock_actual = self.repo_stock.leer_por_producto(producto_id)

    if stock_actual is None:
      if cantidad < 0:
        raise ValueError("No se puede iniciar con stock negativo")
      nuevo_stock = Stock(producto_id, cantidad)
      self.repo_stock.crear(nuevo_stock)
    else:
      stock_actual.cantidad += cantidad
      self.repo_stock.actualizar(stock_actual)

  def obtener_stock(self, producto_id: int) -> int:
    stock = self.repo_stock.leer_por_producto(producto_id)
    return stock.cantidad if stock else 0

class ServicioCotizacionDolar:
  def __init__(self, repo_cotizacion: Any, srv_tipo_cotizacion: Any):
    self.repo_cotizacion = repo_cotizacion
    self.srv_tipo_cotizacion = srv_tipo_cotizacion

  def registrar_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    self.srv_tipo_cotizacion.obtener(cotizacion.tipo.id)
    return self.repo_cotizacion.crear(cotizacion)

  def obtener_historico(self, tipo_id: int) -> List[CotizacionDolar]:
    self.srv_tipo_cotizacion.obtener(tipo_id)
    return self.repo_cotizacion.leer_historico_por_tipo(tipo_id)
