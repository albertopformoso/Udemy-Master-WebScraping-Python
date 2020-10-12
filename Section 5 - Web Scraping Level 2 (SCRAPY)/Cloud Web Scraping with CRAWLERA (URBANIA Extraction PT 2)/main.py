from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Department(Item):
    name = Field()
    direction = Field()


class Urbania(CrawlSpider):
    name = "Departments"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 5,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'INGRESA_TU_API_KEY'
    }

    """
    Este arreglo lo podriamos armar dinamicamente, algo tipo:
    start_urls = []
    for i in range (1, 100):
      start_urls.append('https://urbania.pe/buscar/proyectos-propiedades?page=' + str(i))
    """
    start_urls = [
        'https://urbania.pe/buscar/proyectos-propiedades?page=1',
        'https://urbania.pe/buscar/proyectos-propiedades?page=2',
        'https://urbania.pe/buscar/proyectos-propiedades?page=3',
        'https://urbania.pe/buscar/proyectos-propiedades?page=4',
        'https://urbania.pe/buscar/proyectos-propiedades?page=5'
    ]

    allowed_domains = ['urbania.pe']

    download_delay = 1
    rules = (
        Rule(LinkExtractor(allow=r'/proyecto'), follow=True, callback='parse_depa'),
    )

    def parse_depa(self, response):
        sel = Selector(response)
        item = ItemLoader(Department(), sel)

        item.add_xpath('name', '//*[@id="development-head"]/div[3]/div/div[1]/div[2]/h2[1]/text()')
        item.add_xpath('direction', '//*[@id="development-head"]/div[3]/div/div[1]/div[2]/h2[2]/text()')

        yield item.load_item()