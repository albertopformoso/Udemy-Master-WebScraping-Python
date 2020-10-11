from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Article(Item):
    title = Field()
    content = Field()


class Review(Item):
    title = Field()
    rating = Field()


class Video(Item):
    title = Field()
    publication_date = Field()


class IGNCrawler(CrawlSpider):
    name = 'ign'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'CLOSESPIDER_PAGECOUNT': 50
    }

    allowed_domains = ['latam.ign.com']

    download_delay = 1

    start_urls = ['https://latam.ign.com/se/?model=article&q=ps4']

    rules = (
        # Horizontal by type of info
        Rule(LinkExtractor(allow=r'type='), follow=True),

        # Horizontal by pagination
        Rule(LinkExtractor(allow=r'&page=\d+'), follow=True),

        # Rules by content type with vertical navigation
        # Reviews
        Rule(LinkExtractor(allow=r'/review/'), follow=True, callback='parse_reviews'),

        # Videos
        Rule(LinkExtractor(allow=r'/video/'), follow=True, callback='parse_videos'),

        # Articles
        Rule(LinkExtractor(allow=r'/news/'), follow=True, callback='parse_news'),
    )

    def parse_news(self, response):
        item = ItemLoader(Article(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('content', '//div[@id="id_text"]//*/text()')

        yield item.load_item()

    def parse_reviews(self, response):
        item = ItemLoader(Review(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('rating', '//span[@class="side-wrapper hexagon-content"]/text()')

        yield item.load_item()

    def parse_videos(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_xpath('publication_date', '//span[@class="publish-date"]/text()')

        yield item.load_item()
