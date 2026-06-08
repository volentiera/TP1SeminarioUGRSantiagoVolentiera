import pandas as pd
import json
import os
import pathlib
from datetime import datetime
from price_manager.database.connection import ConexionDB
from sqlalchemy import text

_CSV_DIR = pathlib.Path(__file__).resolve().parent.parent / "migrations" / "csv"
RUTA_JSON = str(_CSV_DIR / "resultados_scraper.json")
RUTA_EXCEL = str(_CSV_DIR / "reporte_precios.xlsx")


def generar_reporte_excel() -> str:
    """Genera un reporte Excel comparando precios internos vs web."""
    if not os.path.exists(RUTA_JSON):
        print("❌ Error: No se encontró el archivo JSON. Ejecutá el scraper primero.")
        return ""

    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        datos_web = json.load(f)

    if not datos_web:
        print("⚠️ El archivo de extracción está vacío.")
        return ""

    db = ConexionDB()
    filas = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with db.transaccion() as connection:
        for item in datos_web:
            prod_id = item.get('producto_id')
            precio_web = float(item.get('precio', 0.0))
            nombre = item.get('nombre_buscado', 'Desconocido')

            query = text("SELECT precio_valor FROM productos WHERE id = :pid")
            resultado = connection.execute(query, {"pid": prod_id}).fetchone()

            precio_interno = float(resultado[0]) if resultado else 0.0
            diferencia = precio_interno - precio_web

            filas.append({
                "Producto": nombre,
                "Precio interno": precio_interno,
                "Precio web": precio_web,
                "Diferencia": diferencia,
                "Fecha de extracción": fecha_actual
            })

    df = pd.DataFrame(filas)
    os.makedirs(os.path.dirname(RUTA_EXCEL), exist_ok=True)
    df.to_excel(RUTA_EXCEL, index=False)
    print(f"✅ Reporte Excel generado correctamente en {RUTA_EXCEL}")
    return RUTA_EXCEL
