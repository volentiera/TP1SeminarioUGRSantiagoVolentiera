import sys
import os
sys.path.insert(0, '/content/price_manager/src')

import json
import re
import requests
from bs4 import BeautifulSoup
from price_manager.database.connection import ConexionDB
from sqlalchemy import text

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36"
    )
}
BASE_URL = "https://www.starcomputacion.com.ar"
RUTA_SALIDA = (
    '/content/price_manager/src/price_manager'
    '/migrations/csv/resultados_scraper.json'
)

# Mapeo: nombre del producto → URL de categoría del sitio
CATEGORIA_MAP = {
    'Monitor Samsung':    'prods/computacin-1/monitores-leds-113/',
    'Mouse Gamer':        'prods/computacin-1/gamers-262/',
    'Teclado Gaming':     'prods/computacin-1/gaming-83/',
    'Auricular Gamer':    'prods/computacin-1/auriculares-gamers-37/',
    'SSD Interno':        'prods/computacin-1/solido-ssd-internos-sata-iii-172/',
    'Pendrive':           'prods/computacin-1/pendrives-9/',
    'Parlante Bluetooth': 'prods/computacin-1/bluetooth-178/',
    'Webcam':             'prods/computacin-1/webcams-28/',
    'Router Wifi':        'prods/computacin-1/router-223/',
    'Smartwatch':         'prods/electronica-2/smartwatch-42/',
}


def limpiar_precio(texto: str) -> float:
    """'ARS 217540' → 217540.0"""
    solo_numeros = re.sub(r"[^\d]", "", str(texto))
    return float(solo_numeros) if solo_numeros else 0.0


def normalizar_img(src: str) -> str:
    if src.startswith("../"):
        return BASE_URL + "/" + src[3:]
    if src.startswith("/"):
        return BASE_URL + src
    return src


def obtener_productos() -> list:
    db = ConexionDB()
    try:
        with db.transaccion() as conn:
            res = conn.execute(
                text("SELECT id, nombre FROM productos LIMIT 10")
            )
            return [(row[0], row[1]) for row in res]
    except Exception as e:
        print(f"Error DB: {e}")
        return []


def scrapear_detalle(url_detalle: str) -> dict:
    """Precio contado, imagen grande, descripción y formas de pago."""
    try:
        r = requests.get(url_detalle, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        precio_tag = soup.select_one("#prices_table .price_td")
        precio = limpiar_precio(precio_tag.text if precio_tag else "0")

        img_tag = soup.select_one(
            "img[src*='files/products']:not([class])"
        )
        url_img = normalizar_img(img_tag["src"] if img_tag else "")

        desc_tag = soup.select_one(".desc_general")
        descripcion = (
            desc_tag.get_text(separator="\n", strip=True)
            if desc_tag else ""
        )

        formas = []
        for fila in soup.select("#prices_table tr"):
            tipo = fila.select_one("td:first-child")
            valor = fila.select_one(".price_td")
            if tipo and valor:
                formas.append(
                    f"{tipo.text.strip()}: {valor.text.strip()}"
                )

        return {
            "precio": precio,
            "url_img": url_img,
            "descripcion": descripcion,
            "formas_pago": " | ".join(formas) if formas else "No disponible",
        }
    except Exception as e:
        print(f"  ⚠️ Error en detalle: {e}")
        return {}


def ejecutar_spider() -> None:
    productos = obtener_productos()
    if not productos:
        print("❌ No hay productos en la base de datos.")
        return

    resultados = []

    for prod_id, nombre in productos:
        # Buscar categoría mapeada, si no existe salteamos
        ruta_cat = CATEGORIA_MAP.get(nombre)
        if not ruta_cat:
            print(f"⚠️  '{nombre}' no tiene categoría mapeada, salteando.")
            continue

        url_categoria = f"{BASE_URL}/{ruta_cat}"
        print(f"\n🔍 [{prod_id}] {nombre} → {url_categoria}")

        try:
            r = requests.get(url_categoria, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            tarjetas = soup.select("a.product")[:10]
            print(f"   {len(tarjetas)} productos encontrados en la categoría")
        except Exception as e:
            print(f"  ⚠️ Error al scrapear categoría: {e}")
            continue

        for tarjeta in tarjetas:
            href = tarjeta.get("href", "")
            url_detalle = f"{BASE_URL}/{href}"

            titulo_tag = tarjeta.select_one(".title")
            precio_tag = tarjeta.select_one(".price")
            img_tag = tarjeta.select_one(".img")

            titulo = titulo_tag.text.strip() if titulo_tag else href
            precio_tarjeta = limpiar_precio(
                precio_tag.text if precio_tag else "0"
            )

            print(f"   🛒 {titulo[:55]}")
            detalle = scrapear_detalle(url_detalle)

            resultados.append({
                "producto_id": prod_id,
                "nombre_buscado": nombre,
                "titulo_web": titulo,
                "precio": detalle.get("precio") or precio_tarjeta,
                "url_img": detalle.get("url_img") or normalizar_img(
                    img_tag["src"] if img_tag else ""
                ),
                "descripcion": detalle.get("descripcion", titulo),
                "formas_pago": detalle.get(
                    "formas_pago", "No disponible"
                ),
            })

    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
    with open(RUTA_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(
        f"\n✅ {len(resultados)} resultados guardados en {RUTA_SALIDA}"
    )


if __name__ == "__main__":
    ejecutar_spider()
