from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy import Request


class Dummy(Item):
    title = Field()
    title_iframe = Field()


class W3SCrawler(CrawlSpider):
    name = "w3s"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    # allowed_domains = ['w3schools.com']
    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']
    download_delay = 1

    def parser(self, response):
        sel = Selector(response)
        title = sel.xpath('//div[@id="main"]//h1/span/text()').get()

        meta_data = {'title': title}

        iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()

        iframe_url = 'https://www.w3schools.com/html/' + iframe_url

        yield Request(iframe_url, callback=self.parse_iframe, meta=meta_data)

    def parse_iframe(self, response):
        item = ItemLoader(Dummy(), response)
        item.add_xpath('title_iframe', '//div[@id="main"]//h1/span/text()')
        item.add_value('title', response.meta.get('title'))

        yield item.load_item()
