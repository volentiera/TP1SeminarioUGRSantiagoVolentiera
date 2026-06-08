import os
import datetime
import requests
from typing import List, Any
from dotenv import load_dotenv

from price_manager.entities.entities import Stock, CotizacionDolar

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()


class ServicioGenerico:
    def __init__(self, repositorio: Any) -> None:
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
    def __init__(self, repo_producto: Any, srv_categoria: Any, srv_proveedor: Any) -> None:
        super().__init__(repo_producto)
        self.srv_categoria = srv_categoria
        self.srv_proveedor = srv_proveedor


class ServicioStock:
    def __init__(self, repo_stock: Any, srv_producto: Any) -> None:
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

    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock para un producto existente."""
        self.srv_producto.obtener(stock.producto_id)
        if self.repo_stock.leer_por_producto(stock.producto_id) is not None:
            raise ValueError(
                f"Ya existe stock para el producto {stock.producto_id}"
            )
        return self.repo_stock.crear(stock)

    def listar_todos(self) -> List[Stock]:
        return self.repo_stock.leer_todos()

    def actualizar(self, stock: Stock) -> Stock:
        """Setea la cantidad del stock al valor indicado."""
        self.srv_producto.obtener(stock.producto_id)
        if self.repo_stock.leer_por_producto(stock.producto_id) is None:
            raise ValueError(
                f"No existe stock para el producto {stock.producto_id}"
            )
        return self.repo_stock.actualizar(stock)

    def eliminar(self, producto_id: int) -> bool:
        if self.repo_stock.leer_por_producto(producto_id) is None:
            raise ValueError(
                f"No existe stock para el producto {producto_id}"
            )
        return self.repo_stock.eliminar(producto_id)


class ServicioCotizacionDolar:
    def __init__(self, repo_cotizacion: Any, srv_tipo_cotizacion: Any) -> None:
        self.repo_cotizacion = repo_cotizacion
        self.srv_tipo_cotizacion = srv_tipo_cotizacion

    def registrar_cotizacion(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        self.srv_tipo_cotizacion.obtener(cotizacion.tipo.id)
        return self.repo_cotizacion.crear(cotizacion)

    def obtener_historico(self, tipo_id: int) -> List[CotizacionDolar]:
        self.srv_tipo_cotizacion.obtener(tipo_id)
        return self.repo_cotizacion.leer_historico_por_tipo(tipo_id)

    def listar_todos(self) -> List[CotizacionDolar]:
        return self.repo_cotizacion.leer_todos()

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza el valor de la cotizacion identificada por (tipo_id, fecha)."""
        self.srv_tipo_cotizacion.obtener(cotizacion.tipo.id)
        return self.repo_cotizacion.actualizar(cotizacion)

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina la cotizacion identificada por (tipo_id, fecha)."""
        self.srv_tipo_cotizacion.obtener(tipo_id)
        return self.repo_cotizacion.eliminar(tipo_id, fecha)

    def obtener_cotizaciones(self) -> None:
        """Busca cotizaciones en la API, las descarga y registra en la BD."""
        api_url = os.getenv("API_URL")
        if not api_url:
            raise ValueError("La variable API_URL no está configurada en el .env")

        # 1. Obtenemos los datos de la API
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            datos_api = response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error al conectar con DolarAPI: {e}")

        # 2. Obtenemos los tipos de cotización que tenemos cargados en la base de datos
        tipos_bd = self.srv_tipo_cotizacion.listar_todos()
        mapa_tipos = {t.nombre.lower(): t for t in tipos_bd}
        fecha_hoy = datetime.date.today()

        # 3. Cruzamos los datos y registramos
        for cotizacion_api in datos_api:
            # La API devuelve el nombre bajo la clave 'nombre' y el precio bajo 'venta'
            nombre_api = cotizacion_api.get("nombre", "").lower()
            valor_venta = float(cotizacion_api.get("venta", 0.0))

            # Buscamos coincidencias (ej. "oficial" en la API coincide con nuestro tipo "Oficial")
            for nombre_bd, tipo_obj in mapa_tipos.items():
                if nombre_api in nombre_bd or nombre_bd in nombre_api:
                    # Para simplificar y evitar múltiples registros iguales el mismo día,
                    # evaluamos que no hayamos guardado uno hoy para este tipo.
                    historico_existente = self.obtener_historico(tipo_obj.id)
                    ya_existe_hoy = any(c.fecha == fecha_hoy for c in historico_existente)

                    if not ya_existe_hoy:
                        nueva_cotizacion = CotizacionDolar(
                            valor=valor_venta,
                            fecha=fecha_hoy,
                            tipo=tipo_obj
                        )
                        self.repo_cotizacion.crear(nueva_cotizacion)
                    break