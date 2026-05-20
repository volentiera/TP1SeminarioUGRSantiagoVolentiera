import os
import csv
from sqlalchemy.sql import text
from price_manager.database.connection import ConexionDB

def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> None:
    """ 
    Lee archivos CSV, genera archivos SQL de inserción y puebla la base de datos.
    """
    # Nos aseguramos de que la carpeta de destino SQL exista
    os.makedirs(carpeta_sqls, exist_ok=True)
    db = ConexionDB()

    # Diccionario para mapear el archivo CSV con su tabla y columnas en la BD
    # Formato: (archivo_csv, nombre_tabla, mapeo_columnas_csv_a_bd)
    migraciones = [
        ("categorias.csv", "categorias", {"id": "id", "nombre": "nombre"}),
        ("proveedores.csv", "proveedores", {"id": "id", "nombre": "nombre", "contacto": "contacto"}),
        ("monedas.csv", "monedas", {"id": "id", "nombre": "nombre"}),
        ("tipos_cotizacion.csv", "tipos_cotizacion", {"id": "id", "nombre": "nombre"}),
        ("productos.csv", "productos", {
            "id": "id", 
            "nombre": "nombre", 
            "descripcion": "descripcion",
            "precio_valor": "precio_valor", 
            "moneda_id": "moneda_id",
            "fecha": "fecha_precio", 
            "cat_id": "categoria_id", 
            "prov_id": "proveedor_id"
        })
    ]

    # Utilizamos el context manager para ejecutar todas las inserciones en una transacción segura
    with db.transaccion() as conn:
        for archivo_csv, nombre_tabla, mapeo in migraciones:
            ruta_csv = os.path.join(carpeta_csvs, archivo_csv)
            ruta_sql = os.path.join(carpeta_sqls, archivo_csv.replace('.csv', '.sql'))

            if not os.path.exists(ruta_csv):
                print(f"⚠️ Archivo no encontrado: {ruta_csv}")
                continue

            lineas_sql = []
            
            # 1. Leemos el CSV
            with open(ruta_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    columnas = list(mapeo.values())
                    valores = []
                    
                    # 2. Preparamos los valores escapando comillas simples para evitar errores SQL
                    for col_csv in mapeo.keys():
                        val_esc = str(row[col_csv]).replace("'", "''")
                        # SQLite es flexible con los tipos de datos, podemos envolver todo en comillas simples
                        valores.append(f"'{val_esc}'")

                    cols_str = ", ".join(columnas)
                    vals_str = ", ".join(valores)
                    
                    # Usamos INSERT OR IGNORE para que no tire error de Primary Key si se corre 2 veces
                    sentencia = f"INSERT OR IGNORE INTO {nombre_tabla} ({cols_str}) VALUES ({vals_str});"
                    lineas_sql.append(sentencia)

            # 3. Guardamos físicamente las sentencias en el archivo .sql
            with open(ruta_sql, mode='w', encoding='utf-8') as f_sql:
                f_sql.write("\n".join(lineas_sql))

            # 4. Ejecutamos las sentencias en la base de datos
            for sentencia in lineas_sql:
                conn.execute(text(sentencia))

            print(f"✅ Migración exitosa: {archivo_csv} -> {nombre_tabla} ({len(lineas_sql)} registros)")
