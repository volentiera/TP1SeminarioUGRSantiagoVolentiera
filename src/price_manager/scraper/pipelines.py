import re
from itemadapter import ItemAdapter

class PriceManagerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # "ARS 217540" → 217540.0
        if adapter.get("precio"):
            solo_numeros = re.sub(r"[^\d]", "", str(adapter["precio"]))
            try:
                adapter["precio"] = float(solo_numeros)
            except ValueError:
                adapter["precio"] = 0.0

        # Normaliza URLs relativas de imagen
        if adapter.get("url_img"):
            url = str(adapter["url_img"])
            if url.startswith("../"):
                adapter["url_img"] = (
                    "https://www.starcomputacion.com.ar/" + url[3:]
                )

        return item
