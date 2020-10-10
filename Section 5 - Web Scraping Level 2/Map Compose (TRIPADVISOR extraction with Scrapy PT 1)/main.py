from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import re


class Hotel(Item):
    name = Field()
    price = Field()
    description = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):
    name = 'Hotels'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    download_delay = 2

    rules = (
        Rule(LinkExtractor(allow=r'/Hotel_Review-'), follow=True, callback='parse_hotel'),
    )

    def removePriceSymbol(self, text):
        newText = text.replace('MX','')
        newText = re.findall(r'\$\d+\,?\d+', newText)
        return newText

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        if not item.get_xpath('//div[contains(@class, "ui_column _3i")]/div/text()'):
            item.add_xpath('price','//div[contains(@data-sizegroup, "hr_chevron_prices")][1]',
                           MapCompose(self.removePriceSymbol))
        else:
            item.add_xpath('price', '//div[contains(@class, "ui_column _3i")]/div/text()',
                           MapCompose(self.removePriceSymbol))
        item.add_xpath('description', '//div[contains(@class, "_2f_ruteS")]/div/text()')
        item.add_xpath('amenities', '//div[@class="_1nAmDotd"][1]/div/text()')

        yield item.load_item()
