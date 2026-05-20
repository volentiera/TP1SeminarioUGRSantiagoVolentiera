import csv
import os
from typing import Any, Dict

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
            print("5. Reportes y Exportación (Bimonetario / CSV)")
            print("0. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1": self._menu_productos()
            elif opcion == "2": self._menu_stock()
            elif opcion == "3": self._menu_maestros()
            elif opcion == "4": self._menu_cotizaciones()
            elif opcion == "5": self._menu_reportes()
            elif opcion == "0": break
            else: print("❌ Opción no válida.")

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
            print("✅ ¡Movimiento registrado con éxito!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def _menu_maestros(self) -> None:
        print("\n--- CATEGORÍAS REGISTRADAS ---")
        for c in self.servicios["categoria"].listar_todos():
            print(f"- {c.nombre} (ID: {c.id})")
        print("\n--- PROVEEDORES REGISTRADOS ---")
        for p in self.servicios["proveedor"].listar_todos():
            print(f"- {p.nombre} (Contacto: {p.contacto})")
        input("\nPresione Enter para volver...")

    def _menu_cotizaciones(self) -> None:
        while True:
            print("\n--- COTIZACIONES DÓLAR ---")
            print("1. Ver históricos por tipo")
            print("2. Obtener cotizaciones por API (DolarAPI)")
            print("0. Volver")
            opc = input("Seleccione: ")

            if opc == "1":
                try:
                    tipo_id = int(input("ID del tipo (1: Oficial, 2: Blue, etc.): "))
                    historial = self.servicios["cotizacion_dolar"].obtener_historico(tipo_id)
                    if not historial:
                        print("⚠️ No hay registros históricos para este tipo.")
                    for h in historial:
                        print(f"Fecha: {h.fecha} | Valor: ${h.valor}")
                except ValueError as e:
                    print(f"❌ Error: {e}")
            elif opc == "2":
                print("\nDescargando cotizaciones desde la API...")
                try:
                    self.servicios["cotizacion_dolar"].obtener_cotizaciones()
                    print("✅ ¡Cotizaciones actualizadas y registradas con éxito!")
                except Exception as e:
                    print(f"❌ Error al obtener cotizaciones: {e}")
            elif opc == "0":
                break

    def _menu_reportes(self) -> None:
        while True:
            print("\n--- REPORTES Y EXPORTACIÓN ---")
            print("1. Ver lista de precios bimonetaria")
            print("2. Exportar precios a archivo CSV")
            print("0. Volver")
            opc = input("Seleccione: ")
            
            if opc == "1":
                self._reporte_bimonetario()
            elif opc == "2":
                self._exportar_csv()
            elif opc == "0":
                break

    def _reporte_bimonetario(self) -> None:
        print("\n--- LISTADO BIMONETARIO ---")
        tipos = self.servicios["tipo_cotizacion"].listar_todos()
        for t in tipos:
            print(f"[{t.id}] {t.nombre}")
        
        try:
            tipo_id = int(input("\nSeleccione el ID de la cotización para la conversión (Ej. Blue): "))
            historial = self.servicios["cotizacion_dolar"].obtener_historico(tipo_id)
            if not historial:
                print("❌ No hay cotizaciones para este tipo. Por favor, actualice mediante DolarAPI (Opción 4 -> 2).")
                return
                
            ultima = historial[-1] # Obtiene la cotización más reciente de la BD
            valor_cot = ultima.valor
            print(f"\nUtilizando {ultima.tipo.nombre} - Valor de conversión: ${valor_cot}")
            print("-" * 65)
            
            for p in self.servicios["producto"].listar_todos():
                moneda_base = p.precio.moneda.nombre
                precio_base = p.precio.valor
                
                # Regla de conversión cruzada
                if moneda_base == "ARS":
                    precio_conv, moneda_conv = precio_base / valor_cot, "USD"
                else:
                    precio_conv, moneda_conv = precio_base * valor_cot, "ARS"
                    
                print(f"[{p.id:2}] {p.nombre[:15]:<15} | Base: {precio_base:>10.2f} {moneda_base} | Equivalente: {precio_conv:>10.2f} {moneda_conv}")
        except ValueError as e:
            print(f"❌ Error de validación: {e}")

    def _exportar_csv(self) -> None:
        print("\n--- EXPORTAR A CSV ---")
        try:
            ruta_exportacion = "/content/price_manager/exportacion_precios.csv"
            tipos = self.servicios["tipo_cotizacion"].listar_todos()
            
            # Buscamos la cotización más reciente de cada tipo que tengamos guardada en BD
            cotizaciones_actuales = {}
            for t in tipos:
                historial = self.servicios["cotizacion_dolar"].obtener_historico(t.id)
                if historial:
                    cotizaciones_actuales[t.nombre] = historial[-1].valor

            if not cotizaciones_actuales:
                print("⚠️ Atención: No hay cotizaciones registradas. Obtenga datos de la API primero para incluir conversiones.")
                
            with open(ruta_exportacion, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Armamos la cabecera dinámicamente con los tipos de dólar existentes
                cabeceras = ["ID", "Producto", "Precio Base", "Moneda Base"]
                for nombre_tipo in cotizaciones_actuales.keys():
                    cabeceras.append(f"Equivalente {nombre_tipo}")
                writer.writerow(cabeceras)
                
                # Escribimos los productos y sus conversiones
                for p in self.servicios["producto"].listar_todos():
                    mb, pb = p.precio.moneda.nombre, p.precio.valor
                    row = [p.id, p.nombre, round(pb, 2), mb]
                    
                    for valor_cot in cotizaciones_actuales.values():
                        if mb == "ARS":
                            row.append(round(pb / valor_cot, 2))
                        else: # Si el precio está en dólares, multiplicamos
                            row.append(round(pb * valor_cot, 2))
                            
                    writer.writerow(row)
                    
            print(f"✅ Exportación exitosa. Archivo CSV guardado en: {ruta_exportacion}")
        except Exception as e:
            print(f"❌ Error al exportar el archivo: {e}")
