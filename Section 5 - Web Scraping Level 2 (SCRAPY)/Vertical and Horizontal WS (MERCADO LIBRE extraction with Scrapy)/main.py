from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import scrapy

class Product(Item):
    title = Field()
    price = Field()
    description = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'MercadoLibreCrawler'
    # CLOSESPIDER_PAGECOUNT closes de crawler when it enters to 20 pages
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 1

    # allowed_domains = ['https://listado.mercadolibre.com.mx', 'https://www.mercadolibre.com.mx/']

    start_urls = ['https://listado.mercadolibre.com.mx/memoria-ram#D[A:memoria%20ram,L:undefined]']

    rules = (
        # Pagination (Horizontal WS)
        Rule(LinkExtractor(allow=r'_Desde_'), follow=True),

        # Product details (Vertical WS)
        Rule(LinkExtractor(allow=r'/memoria-ram-'), follow=True, callback='parse_product'),
    )

    def cleanText(self, text):
        newText = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return newText

    def parse_product(self, response):
        item = ItemLoader(Product(), response)
        item.add_xpath('title','//div[contains(@class, "ui-pdp-header")]/h1[1]/text()', MapCompose(self.cleanText))
        item.add_xpath('description','//p[contains(@class,"ui-pdp-description")]/text()', MapCompose(self.cleanText))
        item.add_xpath('price','//span[@class="price-tag-fraction"]/text()')

        yield item.load_item()
