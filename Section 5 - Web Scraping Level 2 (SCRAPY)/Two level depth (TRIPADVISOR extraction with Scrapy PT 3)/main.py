from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Reviews(Item):
    title = Field()
    rating = Field()
    content = Field()
    author = Field()


class TripAdvisorCrawler(CrawlSpider):
    name = 'TripAdvisorReviews'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'CLOSESPIDER_PAGECOUNT': 100
    }

    allowed_domains = ['tripadvisor.com']

    download_delay = 1

    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    rules = (
        # Hotel Pagination (H)
        Rule(LinkExtractor(allow=r'-oa\d+'), follow=True),

        # Hotel Details (V)
        Rule(LinkExtractor(allow=r'/Hotel_Review-',
                           restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="HotelName"]']),
             follow=True),

        # Reviews Pagination (H)
        Rule(LinkExtractor(allow=r'-or\d+'), follow=True),

        # Profile User Detail (V)
        Rule(LinkExtractor(allow=r'/Profile/',
                           restrict_xpaths=['//div[@data-test-target="reviews-tab"]//a[contains(@class,"ui_header_link")]']),
             follow=True, callback='parse_review'),
    )

    def obtainRating(self, text):
        rating = text.split("_")[-1]


    def parse_review(self, response):
        sel = Selector(response)
        reviews = sel.xpath('//div[@id="content"]/div/div')
        author = sel.xpath('//h1/span/text()').get()

        for review in reviews:
            item = ItemLoader(Reviews(), review)
            item.add_value('author', author)
            item.add_xpath('title', './/div[@class="social-section-review-ReviewSection__title--dTu08 social-section-review-ReviewSection__linked--kI3zg"]/text()')
            item.add_xpath('rating', './/div[contains(@class, "social-section-review")]//span[contains(@class, "ui_bubble_rating")]/@class',
                           MapCompose(self.obtainRating))
            item.add_xpath('content', './/q/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))

            yield item.load_item()