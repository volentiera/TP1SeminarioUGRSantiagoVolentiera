import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def limpiar_texto(valor):
    """Limpia espacios y saltos de línea extraños."""
    if isinstance(valor, str):
        return valor.strip()
    return valor

class ProductoWebItem(scrapy.Item):
    # Datos de control interno
    producto_id = scrapy.Field(output_processor=TakeFirst())
    nombre_buscado = scrapy.Field(output_processor=TakeFirst())

    # Datos solicitados en la rúbrica
    precio = scrapy.Field(
        input_processor=MapCompose(limpiar_texto),
        output_processor=TakeFirst()
    )
    url_img = scrapy.Field(
        output_processor=TakeFirst()
    )
    formas_pago = scrapy.Field(
        input_processor=MapCompose(limpiar_texto),
        output_processor=Join(" | ") # Unimos las formas de pago en un solo string
    )
    descripcion = scrapy.Field(
        input_processor=MapCompose(limpiar_texto),
        output_processor=Join("\n")
    )
