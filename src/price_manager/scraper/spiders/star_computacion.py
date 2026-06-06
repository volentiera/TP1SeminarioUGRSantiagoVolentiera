import scrapy
from scrapy.loader import ItemLoader
from price_manager.scraper.items import ProductoWebItem

# Mapeo de productos internos a categorías reales del sitio.
# El buscador del sitio no filtra por término, por lo que se
# navega directamente por categoría para obtener resultados reales.
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
BASE_URL = 'https://www.starcomputacion.com.ar'


class StarComputacionSpider(scrapy.Spider):
    name = 'star_computacion'
    allowed_domains = ['starcomputacion.com.ar']

    def __init__(self, productos_internos=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.productos_internos = productos_internos or []

    def start_requests(self):
        """Genera un request por categoría para cada producto interno."""
        for prod_id, nombre in self.productos_internos:
            ruta = CATEGORIA_MAP.get(nombre)
            if not ruta:
                self.logger.warning(f"Sin categoría para '{nombre}', salteando.")
                continue
            yield scrapy.Request(
                url=f'{BASE_URL}/{ruta}',
                callback=self.parse,
                meta={'producto_id': prod_id, 'nombre_buscado': nombre}
            )

    def parse(self, response):
        """Extrae tarjetas de la página de categoría y entra al detalle."""
        prod_id = response.meta['producto_id']
        nombre_buscado = response.meta['nombre_buscado']
        tarjetas = response.css('a.product')
        self.logger.info(f"'{nombre_buscado}': {len(tarjetas)} resultados.")

        for tarjeta in tarjetas[:10]:
            url_detalle = tarjeta.css('::attr(href)').get()
            datos_tarjeta = {
                'producto_id': prod_id,
                'nombre_buscado': nombre_buscado,
                'precio': tarjeta.css('.price::text').get('').strip(),
                'url_img': tarjeta.css('.img::attr(src)').get(''),
                'descripcion_corta': tarjeta.css('.title::text').get('').strip(),
            }
            if url_detalle:
                yield response.follow(
                    url_detalle,
                    callback=self.parse_detalle,
                    meta={'datos': datos_tarjeta}
                )

    def parse_detalle(self, response):
        """Extrae precio, imagen, descripción y formas de pago del detalle."""
        datos = response.meta['datos']
        loader = ItemLoader(item=ProductoWebItem(), response=response)

        loader.add_value('producto_id', datos['producto_id'])
        loader.add_value('nombre_buscado', datos['nombre_buscado'])

        loader.add_css('precio', '#prices_table .price_td::text')

        url_img = response.css(
            "img[src*='files/products']:not([class])::attr(src)"
        ).get('')
        loader.add_value(
            'url_img',
            f"{BASE_URL}{url_img}" if url_img else datos['url_img']
        )

        loader.add_css('descripcion', '.desc_general::text')
        if not response.css('.desc_general').get():
            loader.add_value('descripcion', datos['descripcion_corta'])

        formas = []
        for fila in response.css('#prices_table tr'):
            tipo = fila.css('td:first-child::text').get('').strip()
            valor = fila.css('.price_td::text').get('').strip()
            if tipo and valor:
                formas.append(f'{tipo}: {valor}')
        loader.add_value(
            'formas_pago',
            ' | '.join(formas) if formas else 'No disponible'
        )

        yield loader.load_item()
