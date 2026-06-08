import datetime
from typing import List, Optional
from sqlalchemy.sql import text
from price_manager.database.connection import ConexionDB
from price_manager.entities.entities import (
    Categoria, Proveedor, Moneda, TipoCotizacion,
    Precio, Producto, Stock, CotizacionDolar
)


class RepositorioCategoria:
    def __init__(self) -> None:
        self.db = ConexionDB()

    def leer_todos(self) -> List[Categoria]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM categorias"))
            return [Categoria(id=row[0], nombre=row[1]) for row in result]

    def leer_por_id(self, id: int) -> Optional[Categoria]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM categorias WHERE id = :id"), {"id": id}).fetchone()
            return Categoria(id=result[0], nombre=result[1]) if result else None

    def crear(self, entidad: Categoria) -> Categoria:
        with self.db.transaccion() as conn:
            conn.execute(
                text("INSERT INTO categorias (id, nombre) VALUES (:id, :nombre)"),
                {"id": entidad.id, "nombre": entidad.nombre}
            )
        return entidad

    def actualizar(self, entidad: Categoria) -> Categoria:
        with self.db.transaccion() as conn:
            conn.execute(
                text("UPDATE categorias SET nombre = :nombre WHERE id = :id"),
                {"nombre": entidad.nombre, "id": entidad.id}
            )
        return entidad

    def eliminar(self, id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM categorias WHERE id = :id"), {"id": id})
        return True


class RepositorioProveedor:
    def __init__(self) -> None:
        self.db = ConexionDB()

    def leer_todos(self) -> List[Proveedor]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre, contacto FROM proveedores"))
            return [Proveedor(id=row[0], nombre=row[1], contacto=row[2]) for row in result]

    def leer_por_id(self, id: int) -> Optional[Proveedor]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre, contacto FROM proveedores WHERE id = :id"), {"id": id}).fetchone()
            return Proveedor(id=result[0], nombre=result[1], contacto=result[2]) if result else None

    def crear(self, entidad: Proveedor) -> Proveedor:
        with self.db.transaccion() as conn:
            conn.execute(
                text("INSERT INTO proveedores (id, nombre, contacto) VALUES (:id, :nombre, :contacto)"),
                {"id": entidad.id, "nombre": entidad.nombre, "contacto": entidad.contacto}
            )
        return entidad

    def actualizar(self, entidad: Proveedor) -> Proveedor:
        with self.db.transaccion() as conn:
            conn.execute(
                text("UPDATE proveedores SET nombre = :nombre, contacto = :contacto WHERE id = :id"),
                {"nombre": entidad.nombre, "contacto": entidad.contacto, "id": entidad.id}
            )
        return entidad

    def eliminar(self, id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM proveedores WHERE id = :id"), {"id": id})
        return True


class RepositorioMoneda:
    def __init__(self) -> None:
        self.db = ConexionDB()

    def leer_todos(self) -> List[Moneda]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM monedas"))
            return [Moneda(id=row[0], nombre=row[1]) for row in result]

    def leer_por_id(self, id: int) -> Optional[Moneda]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM monedas WHERE id = :id"), {"id": id}).fetchone()
            return Moneda(id=result[0], nombre=result[1]) if result else None

    def crear(self, entidad: Moneda) -> Moneda:
        with self.db.transaccion() as conn:
            conn.execute(
                text("INSERT INTO monedas (id, nombre) VALUES (:id, :nombre)"),
                {"id": entidad.id, "nombre": entidad.nombre}
            )
        return entidad

    def actualizar(self, entidad: Moneda) -> Moneda:
        with self.db.transaccion() as conn:
            conn.execute(
                text("UPDATE monedas SET nombre = :nombre WHERE id = :id"),
                {"nombre": entidad.nombre, "id": entidad.id}
            )
        return entidad

    def eliminar(self, id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM monedas WHERE id = :id"), {"id": id})
        return True


class RepositorioTipoCotizacion:
    def __init__(self) -> None:
        self.db = ConexionDB()

    def leer_todos(self) -> List[TipoCotizacion]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM tipos_cotizacion"))
            return [TipoCotizacion(id=row[0], nombre=row[1]) for row in result]

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre FROM tipos_cotizacion WHERE id = :id"), {"id": id}).fetchone()
            return TipoCotizacion(id=result[0], nombre=result[1]) if result else None

    def crear(self, entidad: TipoCotizacion) -> TipoCotizacion:
        with self.db.transaccion() as conn:
            conn.execute(
                text("INSERT INTO tipos_cotizacion (id, nombre) VALUES (:id, :nombre)"),
                {"id": entidad.id, "nombre": entidad.nombre}
            )
        return entidad

    def actualizar(self, entidad: TipoCotizacion) -> TipoCotizacion:
        with self.db.transaccion() as conn:
            conn.execute(
                text("UPDATE tipos_cotizacion SET nombre = :nombre WHERE id = :id"),
                {"nombre": entidad.nombre, "id": entidad.id}
            )
        return entidad

    def eliminar(self, id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM tipos_cotizacion WHERE id = :id"), {"id": id})
        return True


class RepositorioProducto:
    def __init__(self) -> None:
        self.db = ConexionDB()
        self.repo_cat = RepositorioCategoria()
        self.repo_prov = RepositorioProveedor()
        self.repo_mon = RepositorioMoneda()

    def leer_todos(self) -> List[Producto]:
        productos = []
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT id, nombre, descripcion, precio_valor, moneda_id, fecha_precio, categoria_id, proveedor_id FROM productos"))
            for row in result:
                moneda = self.repo_mon.leer_por_id(row[4])
                precio = Precio(valor=row[3], moneda=moneda, fecha=datetime.datetime.strptime(row[5], '%Y-%m-%d').date() if isinstance(row[5], str) else row[5])
                categoria = self.repo_cat.leer_por_id(row[6])
                proveedor = self.repo_prov.leer_por_id(row[7])
                productos.append(Producto(id=row[0], nombre=row[1], descripcion=row[2], precio=precio, categoria=categoria, proveedor=proveedor))
        return productos

    def leer_por_id(self, id: int) -> Optional[Producto]:
        with self.db.transaccion() as conn:
            row = conn.execute(text("SELECT id, nombre, descripcion, precio_valor, moneda_id, fecha_precio, categoria_id, proveedor_id FROM productos WHERE id = :id"), {"id": id}).fetchone()
            if not row:
                return None
            moneda = self.repo_mon.leer_por_id(row[4])
            precio = Precio(valor=row[3], moneda=moneda, fecha=datetime.datetime.strptime(row[5], '%Y-%m-%d').date() if isinstance(row[5], str) else row[5])
            categoria = self.repo_cat.leer_por_id(row[6])
            proveedor = self.repo_prov.leer_por_id(row[7])
            return Producto(id=row[0], nombre=row[1], descripcion=row[2], precio=precio, categoria=categoria, proveedor=proveedor)

    def crear(self, entidad: Producto) -> Producto:
        with self.db.transaccion() as conn:
            conn.execute(
                text("""INSERT INTO productos (id, nombre, descripcion, precio_valor, moneda_id, fecha_precio, categoria_id, proveedor_id)
                        VALUES (:id, :nom, :desc, :pval, :mid, :fec, :cid, :pid)"""),
                {"id": entidad.id, "nom": entidad.nombre, "desc": entidad.descripcion, "pval": entidad.precio.valor,
                 "mid": entidad.precio.moneda.id, "fec": entidad.precio.fecha, "cid": entidad.categoria.id, "pid": entidad.proveedor.id}
            )
        return entidad

    def actualizar(self, entidad: Producto) -> Producto:
        with self.db.transaccion() as conn:
            conn.execute(
                text("""UPDATE productos SET nombre=:nom, descripcion=:desc, precio_valor=:pval, moneda_id=:mid,
                        fecha_precio=:fec, categoria_id=:cid, proveedor_id=:pid WHERE id=:id"""),
                {"id": entidad.id, "nom": entidad.nombre, "desc": entidad.descripcion, "pval": entidad.precio.valor,
                 "mid": entidad.precio.moneda.id, "fec": entidad.precio.fecha, "cid": entidad.categoria.id, "pid": entidad.proveedor.id}
            )
        return entidad

    def eliminar(self, id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM productos WHERE id = :id"), {"id": id})
        return True


class RepositorioStock:
    def __init__(self) -> None:
        self.db = ConexionDB()

    def leer_todos(self) -> List[Stock]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT producto_id, cantidad FROM stock"))
            return [Stock(producto_id=row[0], cantidad=row[1]) for row in result]

    def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT cantidad FROM stock WHERE producto_id = :id"), {"id": producto_id}).fetchone()
            return Stock(producto_id=producto_id, cantidad=result[0]) if result else None

    def crear(self, stock: Stock) -> Stock:
        with self.db.transaccion() as conn:
            conn.execute(text("INSERT INTO stock (producto_id, cantidad) VALUES (:id, :cant)"),
                         {"id": stock.producto_id, "cant": stock.cantidad})
        return stock

    def actualizar(self, stock: Stock) -> Stock:
        with self.db.transaccion() as conn:
            conn.execute(text("UPDATE stock SET cantidad = :cant WHERE producto_id = :id"),
                         {"cant": stock.cantidad, "id": stock.producto_id})
        return stock

    def eliminar(self, producto_id: int) -> bool:
        with self.db.transaccion() as conn:
            conn.execute(text("DELETE FROM stock WHERE producto_id = :id"), {"id": producto_id})
        return True


class RepositorioCotizacionDolar:
    def __init__(self) -> None:
        self.db = ConexionDB()
        self.repo_tipo = RepositorioTipoCotizacion()

    def leer_todos(self) -> List[CotizacionDolar]:
        cotizaciones = []
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT valor, fecha, tipo_id FROM cotizaciones_dolar ORDER BY fecha ASC, tipo_id ASC"))
            for row in result:
                tipo = self.repo_tipo.leer_por_id(row[2])
                fecha_obj = datetime.datetime.strptime(row[1], '%Y-%m-%d').date() if isinstance(row[1], str) else row[1]
                cotizaciones.append(CotizacionDolar(valor=row[0], fecha=fecha_obj, tipo=tipo))
        return cotizaciones

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        cotizaciones = []
        with self.db.transaccion() as conn:
            result = conn.execute(text("SELECT valor, fecha, tipo_id FROM cotizaciones_dolar WHERE tipo_id = :tid ORDER BY fecha ASC"), {"tid": tipo_id})
            for row in result:
                tipo = self.repo_tipo.leer_por_id(row[2])
                fecha_obj = datetime.datetime.strptime(row[1], '%Y-%m-%d').date() if isinstance(row[1], str) else row[1]
                cotizaciones.append(CotizacionDolar(valor=row[0], fecha=fecha_obj, tipo=tipo))
        return cotizaciones

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        with self.db.transaccion() as conn:
            conn.execute(
                text("INSERT INTO cotizaciones_dolar (valor, fecha, tipo_id) VALUES (:val, :fec, :tid)"),
                {"val": cotizacion.valor, "fec": cotizacion.fecha, "tid": cotizacion.tipo.id}
            )
        return cotizacion

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza el valor de la cotizacion identificada por (tipo_id, fecha)."""
        with self.db.transaccion() as conn:
            conn.execute(
                text("UPDATE cotizaciones_dolar SET valor = :val WHERE tipo_id = :tid AND fecha = :fec"),
                {"val": cotizacion.valor, "tid": cotizacion.tipo.id, "fec": cotizacion.fecha}
            )
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
        """Elimina la cotizacion identificada por (tipo_id, fecha)."""
        with self.db.transaccion() as conn:
            conn.execute(
                text("DELETE FROM cotizaciones_dolar WHERE tipo_id = :tid AND fecha = :fec"),
                {"tid": tipo_id, "fec": fecha}
            )
        return True