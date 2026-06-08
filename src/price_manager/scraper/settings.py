
BOT_NAME = 'price_manager'

SPIDER_MODULES = ['price_manager.scraper.spiders']
NEWSPIDER_MODULE = 'price_manager.scraper.spiders'

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/131.0.0.0 Safari/537.36')

ROBOTSTXT_OBEY = False

# Reemplaza el cliente TLS por curl_cffi para imitar el handshake de Chrome
# y sortear el WAF que devolvia 403 a las requests del cliente Scrapy.
DOWNLOAD_HANDLERS = {
    'http': 'scrapy_impersonate.ImpersonateDownloadHandler',
    'https': 'scrapy_impersonate.ImpersonateDownloadHandler',
}
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS = 2

ITEM_PIPELINES = {
    'price_manager.scraper.pipelines.PriceManagerPipeline': 300,
}

FEED_EXPORT_ENCODING = 'utf-8'
