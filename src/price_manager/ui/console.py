import datetime
from typing import Any, Dict

from price_manager.entities.entities import Categoria, Proveedor, Producto

class InterfazConsola:
    def __init__(self, servicios: Dict[str, Any]):
        self.servicios = servicios

    def iniciar(self) -> None:
        while True:
            print("\n========================================")
            print("   PRICE MANAGER - STAR COMPUTACIÓN")
            print("========================================")
            print("1. Gestionar Categorías (CRUD)")
            print("2. Gestionar Proveedores (CRUD)")
            print("3. Gestionar Productos (CRUD)")
            print("4. Gestionar Stock")
            print("0. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1": self._menu_crud_categorias()
            elif opcion == "2": self._menu_crud_proveedores()
            elif opcion == "3": self._menu_crud_productos()
            elif opcion == "4": self._menu_stock()
            elif opcion == "0": break
            else: print("Opción no válida.")

    # ==========================================
    # CRUD CATEGORÍAS
    # ==========================================
    def _menu_crud_categorias(self) -> None:
        while True:
            print("\n--- GESTIÓN DE CATEGORÍAS ---")
            print("1. Crear Categoría")
            print("2. Listar Categorías")
            print("3. Modificar Categoría")
            print("4. Eliminar Categoría")
            print("0. Volver")
            
            opc = input("Seleccione: ")
            
            if opc == "1":
                try:
                    cat_id = int(input("Ingrese ID de la nueva categoría: "))
                    nombre = input("Ingrese nombre de la categoría: ")
                    nueva_cat = Categoria(id=cat_id, nombre=nombre)
                    self.servicios["categoria"].crear(nueva_cat)
                    print("✅ Categoría creada con éxito.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
            
            elif opc == "2":
                print("\n--- LISTA DE CATEGORÍAS ---")
                for c in self.servicios["categoria"].listar_todos():
                    print(f"[{c.id}] {c.nombre}")
                    
            elif opc == "3":
                try:
                    cat_id = int(input("Ingrese el ID de la categoría a modificar: "))
                    categoria = self.servicios["categoria"].obtener(cat_id)
                    nuevo_nombre = input(f"Nuevo nombre (actual: {categoria.nombre}): ")
                    categoria.nombre = nuevo_nombre
                    self.servicios["categoria"].actualizar(categoria)
                    print("✅ Categoría actualizada con éxito.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "4":
                try:
                    cat_id = int(input("Ingrese el ID de la categoría a eliminar: "))
                    self.servicios["categoria"].eliminar(cat_id)
                    print("✅ Categoría eliminada.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "0":
                break

    # ==========================================
    # CRUD PROVEEDORES
    # ==========================================
    def _menu_crud_proveedores(self) -> None:
        while True:
            print("\n--- GESTIÓN DE PROVEEDORES ---")
            print("1. Crear Proveedor")
            print("2. Listar Proveedores")
            print("3. Modificar Proveedor")
            print("4. Eliminar Proveedor")
            print("0. Volver")
            
            opc = input("Seleccione: ")
            
            if opc == "1":
                try:
                    prov_id = int(input("Ingrese ID: "))
                    nombre = input("Ingrese nombre: ")
                    contacto = input("Ingrese contacto: ")
                    nuevo_prov = Proveedor(id=prov_id, nombre=nombre, contacto=contacto)
                    self.servicios["proveedor"].crear(nuevo_prov)
                    print("✅ Proveedor creado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "2":
                for p in self.servicios["proveedor"].listar_todos():
                    print(f"[{p.id}] {p.nombre} - Contacto: {p.contacto}")
                    
            elif opc == "3":
                try:
                    prov_id = int(input("ID del proveedor a modificar: "))
                    prov = self.servicios["proveedor"].obtener(prov_id)
                    prov.nombre = input(f"Nuevo nombre (actual: {prov.nombre}): ")
                    prov.contacto = input(f"Nuevo contacto (actual: {prov.contacto}): ")
                    self.servicios["proveedor"].actualizar(prov)
                    print("✅ Proveedor actualizado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "4":
                try:
                    prov_id = int(input("ID del proveedor a eliminar: "))
                    self.servicios["proveedor"].eliminar(prov_id)
                    print("✅ Proveedor eliminado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "0":
                break

    # ==========================================
    # CRUD PRODUCTOS
    # ==========================================
    def _menu_crud_productos(self) -> None:
        while True:
            print("\n--- GESTIÓN DE PRODUCTOS ---")
            print("1. Crear Producto")
            print("2. Listar Productos")
            print("3. Modificar Nombre/Descripción de Producto")
            print("4. Eliminar Producto")
            print("0. Volver")
            
            opc = input("Seleccione: ")
            
            if opc == "1":
                try:
                    prod_id = int(input("ID del Producto: "))
                    nombre = input("Nombre: ")
                    desc = input("Descripción: ")
                    
                    # Para simplificar el alta en CLI, asumimos que usa una categoría y proveedor existentes
                    cat_id = int(input("ID de Categoría existente: "))
                    prov_id = int(input("ID de Proveedor existente: "))
                    
                    categoria = self.servicios["categoria"].obtener(cat_id)
                    proveedor = self.servicios["proveedor"].obtener(prov_id)
                    
                    # El precio requiere Moneda y Fecha, lo ideal sería solicitarlo o instanciarlo
                    # Aquí lo pasamos temporalmente como None para fines prácticos, o deberías pedirlo
                    print("⚠️  Nota: Para asignar precio, utilice el módulo económico.")
                    
                    nuevo_prod = Producto(id=prod_id, nombre=nombre, descripcion=desc, 
                                          precio=None, categoria=categoria, proveedor=proveedor)
                    self.servicios["producto"].crear(nuevo_prod)
                    print("✅ Producto creado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "2":
                for p in self.servicios["producto"].listar_todos():
                    cat_nombre = p.categoria.nombre if p.categoria else "Sin categoría"
                    print(f"[{p.id}] {p.nombre} ({cat_nombre}) - {p.descripcion}")
                    
            elif opc == "3":
                try:
                    prod_id = int(input("ID del producto a modificar: "))
                    prod = self.servicios["producto"].obtener(prod_id)
                    prod.nombre = input(f"Nuevo nombre (actual: {prod.nombre}): ")
                    prod.descripcion = input(f"Nueva descripción (actual: {prod.descripcion}): ")
                    self.servicios["producto"].actualizar(prod)
                    print("✅ Producto actualizado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "4":
                try:
                    prod_id = int(input("ID del producto a eliminar: "))
                    self.servicios["producto"].eliminar(prod_id)
                    print("✅ Producto eliminado.")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opc == "0":
                break

    # ==========================================
    # GESTIÓN DE STOCK (Mantenemos la que tenías)
    # ==========================================
    def _menu_stock(self) -> None:
        print("\n--- GESTIÓN DE STOCK ---")
        try:
            id_prod = int(input("Ingrese ID del producto: "))
            actual = self.servicios["stock"].obtener_stock(id_prod)
            print(f"Stock actual: {actual}")

            cambio = int(input("Cantidad a ajustar (use números negativos para restar): "))
            self.servicios["stock"].registrar_movimiento(id_prod, cambio)
            print("✅ ¡Movimiento registrado con éxito!")
        except ValueError as e:
            print(f"❌ Error: {e}")
