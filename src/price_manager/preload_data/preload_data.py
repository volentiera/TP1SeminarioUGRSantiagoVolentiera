
import csv
import datetime
from typing import Any, List, Dict

from price_manager.entities.entities import (
  Categoria, Proveedor, Moneda, TipoCotizacion, Precio, Producto
)

def leer_csv(nombre_archivo: str) -> List[Dict[str, str]]:
  ruta = f"price_manager/migrations/csv/{nombre_archivo}"
  filas = []
  try:
    with open(ruta, mode='r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for fila in reader:
        filas.append(fila)
  except FileNotFoundError:
    pass
  return filas

def cargar_datos(servicios: Dict[str, Any]) -> None:
  for row in leer_csv("categorias.csv"):
    cat = Categoria(id=int(row["id"]), nombre=row["nombre"])
    try: servicios["categoria"].crear(cat)
    except ValueError: pass

  for row in leer_csv("proveedores.csv"):
    prov = Proveedor(
      id=int(row["id"]), nombre=row["nombre"], contacto=row["contacto"]
    )
    try: servicios["proveedor"].crear(prov)
    except ValueError: pass

  for row in leer_csv("monedas.csv"):
    mon = Moneda(id=int(row["id"]), nombre=row["nombre"])
    try: servicios["moneda"].crear(mon)
    except ValueError: pass

  for row in leer_csv("tipos_cotizacion.csv"):
    tipo = TipoCotizacion(id=int(row["id"]), nombre=row["nombre"])
    try: servicios["tipo_cotizacion"].crear(tipo)
    except ValueError: pass

  for row in leer_csv("productos.csv"):
    fecha_obj = datetime.datetime.strptime(row["fecha"], "%Y-%m-%d").date()
    moneda_obj = servicios["moneda"].obtener(int(row["moneda_id"]))
    precio = Precio(valor=float(row["precio_valor"]), moneda=moneda_obj, fecha=fecha_obj)

    cat_obj = servicios["categoria"].obtener(int(row["cat_id"]))
    prov_obj = servicios["proveedor"].obtener(int(row["prov_id"]))

    prod = Producto(
      id=int(row["id"]),
      nombre=row["nombre"],
      descripcion=row["descripcion"],
      precio=precio,
      categoria=cat_obj,
      proveedor=prov_obj
    )
    try: servicios["producto"].crear(prod)
    except ValueError: pass
