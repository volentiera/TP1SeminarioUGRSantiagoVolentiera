import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import text
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from price_manager.database.connection import ConexionDB
from price_manager.scraper import settings as settings_scraper
from price_manager.scraper.spiders.star_computacion import StarComputacionSpider

RUTA_SALIDA = str(
    pathlib.Path(__file__).resolve().parent.parent
    / "migrations" / "csv" / "resultados_scraper.json"
)


def obtener_productos():
    db = ConexionDB()
    with db.transaccion() as conn:
        resultado = conn.execute(
            text("SELECT id, nombre FROM productos LIMIT 10"))
        return [(fila[0], fila[1]) for fila in resultado]


def ejecutar_spider():
    productos = obtener_productos()
    if not productos:
        print("Sin productos en la base.")
        return

    configuracion = Settings()
    configuracion.setmodule(settings_scraper)
    configuracion.set("FEED_STORE_EMPTY", True)
    configuracion.set("FEEDS", {
        RUTA_SALIDA: {
            "format": "json",
            "encoding": "utf-8",
            "overwrite": True,
            "indent": 2,
        }
    })

    proceso = CrawlerProcess(configuracion)
    proceso.crawl(StarComputacionSpider, productos_internos=productos)
    proceso.start()
    print(f"Resultados guardados en {RUTA_SALIDA}")


if __name__ == "__main__":
    ejecutar_spider()
