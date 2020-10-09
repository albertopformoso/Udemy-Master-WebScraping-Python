from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Question(Item):
    id = Field()
    question = Field()
    # description = Field()

class StackOverflowSpider(Spider):
    name = "SO_Spider"
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        questions_list = sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        i=1
        for q in questions_list:
            item = ItemLoader(Question(), q)
            item.add_xpath('question', './/h3/a/text()')
            # item.add_xpath('description', './/div[@class="excerpt"]/text()')
            item.add_value('id', i)
            i += 1

            yield item.load_item()

# To run this script open the terminal and type: scrapy runspider main.py -o spider.csv -t csv