from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class News(Item):
    head = Field()
    description = Field()

class ElUniversoSpider(Spider):
    name = 'EU_Spider'
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    start_urls = ['https://www.eluniverso.com/deportes']

    # Using Scrapy Selector:
    # def parse(self, response):
    #     sel = Selector(response)
    #     news = sel.xpath('//div[@class="view-content"]/div[@class="posts"]')
    #
    #     for n in news:
    #         item = ItemLoader(News(), n)
    #         item.add_xpath('head','.//h2/a/text()')
    #         item.add_xpath('description','.//p/text()')
    #
    #         yield item.load_item()

    # Using BeautifulSoup:
    def parse(self, response):
        soup = BeautifulSoup(response.body)
        news_container = soup.findAll('div', {'class': 'view-content'})

        for container in news_container:
            # Recursive is to indicate if you want to search directrly on the sons
            news = container.findAll('div', class_='posts', recursive=False)
            for n in news:
                item = ItemLoader(News(), response.body)

                head = n.find('h2').text

                # Option 1 for None values
                # try:
                #     descr = n.find('p').text
                # except:
                #     descr = 'N/A'

                # Option 2 for None values
                descr = n.find('p')
                if (descr != None):
                    descr = descr.text
                else:
                    descr = 'N/A'

                item.add_value('head', head)
                item.add_value('description', descr)

                yield item.load_item()

