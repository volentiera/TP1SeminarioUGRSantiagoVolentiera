
BOT_NAME = 'price_manager'

SPIDER_MODULES = ['price_manager.scraper.spiders']
NEWSPIDER_MODULE = 'price_manager.scraper.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

ROBOTSTXT_OBEY = False

# Activamos nuestro Pipeline
ITEM_PIPELINES = {
   'price_manager.scraper.pipelines.PriceManagerPipeline': 300,
}

# Configuración de codificación para evitar problemas con tildes o ñ en los CSV
FEED_EXPORT_ENCODING = 'utf-8'
