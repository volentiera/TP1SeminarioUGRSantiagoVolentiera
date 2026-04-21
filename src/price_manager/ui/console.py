import datetime
from typing import Any, Dict, List

class InterfazConsola:
  def __init__(self, servicios: Dict[str, Any]):
    self.servicios = servicios

  def iniciar(self) -> None:
    while True:
      print("\n========================================")
      print("   PRICE MANAGER - STAR COMPUTACIÓN")
      print("========================================")
      print("1. Gestionar Inventario (Productos)")
      print("2. Gestionar Stock")
      print("3. Consultar Categorías y Proveedores")
      print("4. Gestión Económica (Dólar)")
      print("0. Salir")

      opcion = input("\nSeleccione una opción: ")

      if opcion == "1": self._menu_productos()
      elif opcion == "2": self._menu_stock()
      elif opcion == "3": self._menu_maestros()
      elif opcion == "4": self._menu_cotizaciones()
      elif opcion == "0": break
      else: print("Opción no válida.")

  def _menu_productos(self) -> None:
    print("\n--- PRODUCTOS ---")
    productos = self.servicios["producto"].listar_todos()
    for p in productos:
      print(f"[{p.id}] {p.nombre} - {p.precio.moneda.nombre}: {p.precio.valor}")

    input("\nPresione Enter para continuar...")

  def _menu_stock(self) -> None:
    print("\n--- GESTIÓN DE STOCK ---")
    try:
      id_prod = int(input("Ingrese ID del producto: "))
      actual = self.servicios["stock"].obtener_stock(id_prod)
      print(f"Stock actual: {actual}")

      cambio = int(input("Cantidad a ajustar (use números negativos para restar): "))
      self.servicios["stock"].registrar_movimiento(id_prod, cambio)
      print("¡Movimiento registrado con éxito!")
    except ValueError as e:
      print(f"Error: {e}")

  def _menu_maestros(self) -> None:
    print("\n--- CATEGORÍAS REGISTRADAS ---")
    for c in self.servicios["categoria"].listar_todos():
      print(f"- {c.nombre} (ID: {c.id})")

    print("\n--- PROVEEDORES REGISTRADOS ---")
    for p in self.servicios["proveedor"].listar_todos():
      print(f"- {p.nombre} (Contacto: {p.contacto})")

    input("\nPresione Enter para volver...")

  def _menu_cotizaciones(self) -> None:
    print("\n--- COTIZACIONES DÓLAR ---")
    print("1. Ver históricos por tipo")
    print("2. Registrar nueva cotización")
    opc = input("Seleccione: ")

    if opc == "1":
      tipo_id = int(input("ID del tipo (1: Oficial, 2: Blue, etc.): "))
      try:
        historial = self.servicios["cotizacion_dolar"].obtener_historico(tipo_id)
        for h in historial:
          print(f"Fecha: {h.fecha} | Valor: ${h.valor}")
      except ValueError as e:
        print(e)
    elif opc == "2":
      print("Funcionalidad de carga manual en desarrollo...")
