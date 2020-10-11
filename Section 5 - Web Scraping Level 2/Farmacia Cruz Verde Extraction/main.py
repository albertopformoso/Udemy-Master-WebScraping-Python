from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class DrugStore(Item):
    name = Field()
    price = Field()


class CruzVerde(CrawlSpider):
    name = "DrugStore"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'CLOSESPIDER_PAGECOUNT': 30
    }

    allowed_domains = ["cruzverde.cl"]

    start_urls = ["https://www.cruzverde.cl/medicamentos/"]

    download_delay = 1

    rules = (
        Rule(LinkExtractor(allow=r'start=',
                           tags=('a', 'button'),
                           attrs=('href', 'data-url')),
             follow=True, callback='parse_store'),
    )

    def parse_store(self, response):
        sel = Selector(response)
        products = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for product in products:
            item = ItemLoader(DrugStore(), product)
            item.add_xpath('name', './/div[@class="pdp-link"]/a/text()', MapCompose(lambda i: i.replace('\n','').replace('\r','').strip()))
            item.add_xpath('price', './/span[@class="value"]/text()', MapCompose(lambda i: i.replace('\n','').replace('\r','').strip()))

            yield item.load_item()
