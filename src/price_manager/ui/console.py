from typing import Dict, Any
from price_manager.entities.entities import Categoria, Proveedor, Moneda, TipoCotizacion

class Consola:
    def __init__(self, servicios: Dict[str, Any]) -> None:
        self.servicios = servicios

    def mostrar_menu_principal(self) -> None:
        while True:
            print("\n--- Menú Principal - Price Manager ---")
            print("1. Gestionar Categorías")
            print("2. Gestionar Proveedores")
            print("3. Gestionar Monedas")
            print("4. Gestionar Tipos de Cotización")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.menu_crud("Categoría", self.servicios['categoria'], Categoria)
            elif opcion == '2':
                self.menu_crud("Proveedor", self.servicios['proveedor'], Proveedor)
            elif opcion == '3':
                self.menu_crud("Moneda", self.servicios['moneda'], Moneda)
            elif opcion == '4':
                self.menu_crud("Tipo de Cotización", self.servicios['tipo_cotizacion'], TipoCotizacion)
            elif opcion == '5':
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def menu_crud(self, nombre_entidad: str, servicio: Any, clase_entidad: Any) -> None:
        while True:
            print(f"\n--- Gestionar {nombre_entidad} ---")
            print("1. Crear")
            print("2. Listar todos")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Volver al Menú Principal")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                try:
                    id_val = int(input("Ingrese ID: "))
                    nombre_val = input("Ingrese Nombre: ")
                    if nombre_entidad == "Proveedor":
                        contacto = input("Ingrese Contacto: ")
                        nueva_entidad = clase_entidad(id=id_val, nombre=nombre_val, contacto=contacto)
                    else:
                        nueva_entidad = clase_entidad(id=id_val, nombre=nombre_val)
                    servicio.crear(nueva_entidad)
                    print(f"✅ {nombre_entidad} creada con éxito.")
                except Exception as e:
                    print(f"❌ Error al crear: {e}")

            elif opcion == '2':
                entidades = servicio.listar_todos()
                if not entidades:
                    print(f"No hay registros de {nombre_entidad}.")
                else:
                    for e in entidades:
                        if nombre_entidad == "Proveedor":
                            print(f"ID: {e.id} | Nombre: {e.nombre} | Contacto: {e.contacto}")
                        else:
                            print(f"ID: {e.id} | Nombre: {e.nombre}")

            elif opcion == '3':
                try:
                    id_val = int(input("Ingrese el ID del registro a actualizar: "))
                    nombre_val = input("Ingrese el nuevo Nombre: ")
                    if nombre_entidad == "Proveedor":
                        contacto = input("Ingrese el nuevo Contacto: ")
                        entidad_act = clase_entidad(id=id_val, nombre=nombre_val, contacto=contacto)
                    else:
                        entidad_act = clase_entidad(id=id_val, nombre=nombre_val)
                    servicio.actualizar(entidad_act)
                    print(f"✅ {nombre_entidad} actualizada con éxito.")
                except Exception as e:
                    print(f"❌ Error al actualizar: {e}")

            elif opcion == '4':
                try:
                    id_val = int(input("Ingrese el ID del registro a eliminar: "))
                    servicio.eliminar(id_val)
                    print(f"✅ {nombre_entidad} eliminada con éxito.")
                except Exception as e:
                    print(f"❌ Error al eliminar: {e}")

            elif opcion == '5':
                break
            else:
                print("Opción inválida.")