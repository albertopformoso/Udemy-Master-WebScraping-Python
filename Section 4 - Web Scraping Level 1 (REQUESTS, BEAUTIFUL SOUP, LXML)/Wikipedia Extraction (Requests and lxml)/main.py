import requests
from lxml import html

# Headers
# user-agent
headers = {
    'user-agent': "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
}

url = 'https://www.wikipedia.org'

response = requests.get(url, headers=headers)

parser = html.fromstring(response.text)

#Option 1
# en = parser.get_element_by_id("js-link-box-en")
# print(en.text_content())

#Option 2
# en = parser.xpath('//a[@id="js-link-box-en"]/strong/text()')
# print(en)

#Option 3
# lang = parser.xpath('//div[contains(@class, "central-featured-lang")]//strong/text()')
# for l in lang:
#     print(l)

#Option 4
lang = parser.find_class('central-featured-lang')
for l in lang:
    print(l.text_content())