from typing import Any, Dict

from price_manager.repositories.repositories import (
  RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
  RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock,
  RepositorioCotizacionDolar
)
from price_manager.services.services import (
  ServicioCategoria, ServicioProveedor, ServicioMoneda,
  ServicioTipoCotizacion, ServicioProducto, ServicioStock,
  ServicioCotizacionDolar
)
from price_manager.preload_data.preload_data import cargar_datos
from price_manager.ui.console import InterfazConsola

def main(import_default_data: bool = True) -> None:
  """Función principal que orquestra el inicio del sistema."""

  # 1. Instanciación de Repositorios (Capa de Datos)
  repos = {
    "categoria": RepositorioCategoria(),
    "proveedor": RepositorioProveedor(),
    "moneda": RepositorioMoneda(),
    "tipo_cotizacion": RepositorioTipoCotizacion(),
    "producto": RepositorioProducto(),
    "stock": RepositorioStock(),
    "cotizacion_dolar": RepositorioCotizacionDolar()
  }

  # 2. Instanciación de Servicios (Capa de Lógica)
  # Se inyectan las dependencias necesarias según la arquitectura
  servicios = {
    "categoria": ServicioCategoria(repos["categoria"]),
    "proveedor": ServicioProveedor(repos["proveedor"]),
    "moneda": ServicioMoneda(repos["moneda"]),
    "tipo_cotizacion": ServicioTipoCotizacion(repos["tipo_cotizacion"])
  }

  # Servicios con dependencias cruzadas
  servicios["producto"] = ServicioProducto(
    repos["producto"], servicios["categoria"], servicios["proveedor"]
  )
  servicios["stock"] = ServicioStock(repos["stock"], servicios["producto"])
  servicios["cotizacion_dolar"] = ServicioCotizacionDolar(
    repos["cotizacion_dolar"], servicios["tipo_cotizacion"]
  )

  # 3. Precarga de datos desde CSV si se solicita
  if import_default_data:
    cargar_datos(servicios)

  # 4. Inicio de la Interfaz de Usuario
  ui = InterfazConsola(servicios)
  ui.iniciar()

if __name__ == "__main__":
  main()
