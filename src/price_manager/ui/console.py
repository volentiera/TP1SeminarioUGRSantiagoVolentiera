import csv
import os
from typing import Any, Dict
from google.colab import files

from price_manager.entities.entities import Categoria, Proveedor, Moneda, TipoCotizacion
from price_manager.services.alertas import generar_alertas_csv
from price_manager.services.reporte_excel import generar_reporte_excel
from price_manager.services.auditoria import auditar, obtener_historial_auditoria


class InterfazConsola:
    def __init__(self, servicios: Dict[str, Any]) -> None:
        self.servicios = servicios

    def _descargar_archivos(self) -> None:
        """Descarga los archivos generados al salir del programa."""
        ARCHIVOS = [
            '/content/price_manager/src/price_manager/migrations/csv/alertas_precios.csv',
            '/content/price_manager/src/price_manager/migrations/csv/reporte_precios.xlsx',
        ]
        for ruta in ARCHIVOS:
            if os.path.exists(ruta):
                print(f"⬇️ Descargando {os.path.basename(ruta)}...")
                files.download(ruta)

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
            print("6. Gestionar Entidades (Soporte CRUD)")
            print("--- SPRINT 3 ---")
            print("7. Ejecutar Scraping y Alertas")
            print("8. Generar Reporte Excel de Competencia")
            print("9. Ver Historial de Auditoría")
            print("0. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == "1": self._menu_productos()
            elif opcion == "2": self._menu_stock()
            elif opcion == "3": self._menu_maestros()
            elif opcion == "4": self._menu_cotizaciones()
            elif opcion == "5": self._menu_reportes()
            elif opcion == "6": self._menu_crud_principal()
            elif opcion == "7": self._menu_scraping_alertas()
            elif opcion == "8": self._menu_reporte_excel()
            elif opcion == "9": self._menu_auditoria()
            elif opcion == "0":
                self._descargar_archivos()
                break
            else: print("❌ Opción no válida.")

    # --- SPRINT 3 ---

    @auditar(accion="Scraping Web y Generación de Alertas")
    def _menu_scraping_alertas(self) -> None:
        print("\n--- EJECUTANDO SCRAPER ---")
        os.system("python price_manager/scraper/run_scraper.py")

        try:
            print("\n--- GENERANDO ALERTAS CSV ---")
            umbral = float(
                input("Ingrese la diferencia mínima en pesos para la alerta: ")
            )
            generar_alertas_csv(umbral)
        except ValueError:
            print("❌ Número inválido. Operación cancelada.")
        input("\nPresione Enter para continuar...")

    @auditar(accion="Generación de Reporte Excel")
    def _menu_reporte_excel(self) -> None:
        print("\n--- REPORTE EXCEL DE PRECIOS ---")
        generar_reporte_excel()
        input("\nPresione Enter para continuar...")

    def _menu_auditoria(self) -> None:
        print("\n--- HISTORIAL DE AUDITORÍA ---")
        historial = obtener_historial_auditoria()
        if not historial:
            print("⚠️ No hay registros de auditoría almacenados.")
        else:
            for h in historial:
                print(f"[{h['fecha']}] Acción: {h['accion']} | {h['detalles']}")
        input("\nPresione Enter para volver...")

    # --- FUNCIONES EXISTENTES ---

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
            cambio = int(
                input("Cantidad a ajustar (use números negativos para restar): ")
            )
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
                    historial = self.servicios["cotizacion_dolar"].obtener_historico(
                        tipo_id
                    )
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

            if opc == "1": self._reporte_bimonetario()
            elif opc == "2": self._exportar_csv()
            elif opc == "0": break

    def _reporte_bimonetario(self) -> None:
        print("\n--- LISTADO BIMONETARIO ---")
        tipos = self.servicios["tipo_cotizacion"].listar_todos()
        for t in tipos:
            print(f"[{t.id}] {t.nombre}")

        try:
            tipo_id = int(
                input("\nSeleccione el ID de la cotización para la conversión (Ej. Blue): ")
            )
            historial = self.servicios["cotizacion_dolar"].obtener_historico(tipo_id)
            if not historial:
                print("❌ No hay cotizaciones para este tipo. Por favor, actualice mediante DolarAPI.")
                return

            ultima = historial[-1]
            valor_cot = ultima.valor
            print(f"\nUtilizando {ultima.tipo.nombre} - Valor de conversión: ${valor_cot}")
            print("-" * 65)

            for p in self.servicios["producto"].listar_todos():
                moneda_base = p.precio.moneda.nombre
                precio_base = p.precio.valor
                if moneda_base == "ARS":
                    precio_conv, moneda_conv = precio_base / valor_cot, "USD"
                else:
                    precio_conv, moneda_conv = precio_base * valor_cot, "ARS"
                print(
                    f"[{p.id:2}] {p.nombre[:15]:<15} | "
                    f"Base: {precio_base:>10.2f} {moneda_base} | "
                    f"Equivalente: {precio_conv:>10.2f} {moneda_conv}"
                )
        except ValueError as e:
            print(f"❌ Error de validación: {e}")

    def _exportar_csv(self) -> None:
        print("\n--- EXPORTAR A CSV ---")
        try:
            ruta_exportacion = "exportacion_precios.csv"
            tipos = self.servicios["tipo_cotizacion"].listar_todos()

            cotizaciones_actuales = {}
            for t in tipos:
                historial = self.servicios["cotizacion_dolar"].obtener_historico(t.id)
                if historial:
                    cotizaciones_actuales[t.nombre] = historial[-1].valor

            if not cotizaciones_actuales:
                print("⚠️ Atención: No hay cotizaciones registradas. Obtenga datos de la API primero.")

            with open(ruta_exportacion, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                cabeceras = ["ID", "Producto", "Precio Base", "Moneda Base"]
                for nombre_tipo in cotizaciones_actuales.keys():
                    cabeceras.append(f"Equivalente {nombre_tipo}")
                writer.writerow(cabeceras)

                for p in self.servicios["producto"].listar_todos():
                    mb, pb = p.precio.moneda.nombre, p.precio.valor
                    row = [p.id, p.nombre, round(pb, 2), mb]
                    for valor_cot in cotizaciones_actuales.values():
                        if mb == "ARS":
                            row.append(round(pb / valor_cot, 2))
                        else:
                            row.append(round(pb * valor_cot, 2))
                    writer.writerow(row)

            print("✅ Exportación exitosa. Archivo CSV guardado.")
        except Exception as e:
            print(f"❌ Error al exportar el archivo: {e}")

    def _menu_crud_principal(self) -> None:
        while True:
            print("\n--- Gestionar Entidades (CRUD) ---")
            print("1. Gestionar Categorías")
            print("2. Gestionar Proveedores")
            print("3. Gestionar Monedas")
            print("4. Gestionar Tipos de Cotización")
            print("5. Volver al Menú Principal")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self._menu_crud_entidad("Categoría", self.servicios['categoria'], Categoria)
            elif opcion == '2':
                self._menu_crud_entidad("Proveedor", self.servicios['proveedor'], Proveedor)
            elif opcion == '3':
                self._menu_crud_entidad("Moneda", self.servicios['moneda'], Moneda)
            elif opcion == '4':
                self._menu_crud_entidad(
                    "Tipo de Cotización", self.servicios['tipo_cotizacion'], TipoCotizacion
                )
            elif opcion == '5':
                break
            else:
                print("Opción inválida.")

    def _menu_crud_entidad(
        self, nombre_entidad: str, servicio: Any, clase_entidad: Any
    ) -> None:
        while True:
            print(f"\n--- {nombre_entidad} ---")
            print("1. Crear")
            print("2. Listar todos")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Volver")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                try:
                    id_val = int(input("Ingrese ID: "))
                    nombre_val = input("Ingrese Nombre: ")
                    if nombre_entidad == "Proveedor":
                        contacto = input("Ingrese Contacto: ")
                        nueva_entidad = clase_entidad(
                            id=id_val, nombre=nombre_val, contacto=contacto
                        )
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
                            print(
                                f"ID: {e.id} | Nombre: {e.nombre} | Contacto: {e.contacto}"
                            )
                        else:
                            print(f"ID: {e.id} | Nombre: {e.nombre}")
            elif opcion == '3':
                try:
                    id_val = int(input("Ingrese el ID del registro a actualizar: "))
                    nombre_val = input("Ingrese el nuevo Nombre: ")
                    if nombre_entidad == "Proveedor":
                        contacto = input("Ingrese el nuevo Contacto: ")
                        entidad_act = clase_entidad(
                            id=id_val, nombre=nombre_val, contacto=contacto
                        )
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
