import requests
from lxml import html

headers = {'user-agent': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

login_form_url = 'https://github.com/login'

session = requests.Session()

login_form_res = session.get(login_form_url, headers=headers)

parser = html.fromstring(login_form_res.text)
token = parser.xpath('//input[@name="authenticity_token"]/@value')

login_url = 'https://github.com/session'
login_data = {
    'login': 'XXX',
    'password': 'XXX',
    'commit': 'Sign in',
    'authenticity_token': token
}

session.post(login_url, data=login_data, headers=headers)

data_url = 'https://github.com/albertopformoso?tab=repositories'
response = session.get(data_url, headers=headers)

parser = html.fromstring(response.text)
repositories = parser.xpath('//h3[@class="wb-break-all"]/a/text()')

for repository in repositories:
    print(repository)

