import json
import csv
import os
import pathlib
from datetime import datetime
from price_manager.database.connection import ConexionDB
from sqlalchemy import text

_CSV_DIR = pathlib.Path(__file__).resolve().parent.parent / "migrations" / "csv"

def generar_alertas_csv(umbral_diferencia: float) -> str:
    ruta_json = str(_CSV_DIR / "resultados_scraper.json")
    ruta_csv = str(_CSV_DIR / "alertas_precios.csv")

    if not os.path.exists(ruta_json):
        print("❌ Error: No se encontró el archivo JSON.")
        return ""

    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos_web = json.load(f)

    if not datos_web:
        print("⚠️ El archivo JSON está vacío. Star Computación no devolvió resultados para los nombres de tus productos.")
        return ""

    db = ConexionDB()
    alertas = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n📊 --- DETALLE DE COMPARACIÓN ---")
    with db.transaccion() as connection:
        for item in datos_web:
            prod_id = item.get('producto_id')
            precio_web = float(item.get('precio', 0.0))
            nombre = item.get('nombre_buscado', 'Desconocido')

            query = text("SELECT precio_valor FROM productos WHERE id = :pid")
            resultado = connection.execute(query, {"pid": prod_id}).fetchone()

            if resultado:
                precio_interno = float(resultado[0])
                diferencia = abs(precio_interno - precio_web)

                # Mostramos en pantalla exactamente qué números está restando
                print(f"🔍 {nombre}: Interno ${precio_interno} | Web ${precio_web} | Dif: ${diferencia:.2f}")

                if diferencia >= umbral_diferencia:
                    alertas.append({
                        'producto_id': prod_id,
                        'nombre': nombre,
                        'precio_interno': precio_interno,
                        'precio_web': precio_web,
                        'diferencia': diferencia,
                        'fecha_alerta': fecha_actual
                    })

    if not alertas:
        print(f"\n✅ Todo en orden: No hay diferencias mayores a ${umbral_diferencia}.")
        return ""

    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
    with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
        campos = ['producto_id', 'nombre', 'precio_interno', 'precio_web', 'diferencia', 'fecha_alerta']
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(alertas)

    print(f"\n🚨 Éxito: Se generaron {len(alertas)} alertas en {ruta_csv}")
    return ruta_csv
