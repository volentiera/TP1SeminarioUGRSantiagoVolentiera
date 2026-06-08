
BOT_NAME = 'price_manager'

SPIDER_MODULES = ['price_manager.scraper.spiders']
NEWSPIDER_MODULE = 'price_manager.scraper.spiders'

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/131.0.0.0 Safari/537.36')

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True

ITEM_PIPELINES = {
    'price_manager.scraper.pipelines.PriceManagerPipeline': 300,
}

FEED_EXPORT_ENCODING = 'utf-8'
