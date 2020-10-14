import schedule
import time
from selenium import webdriver

from pymongo import MongoClient  # pip install pymongo

client = MongoClient('localhost')
db = client['weather']
col = db['clima']

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]


def extraer_datos():
    driver = webdriver.Chrome()

    for url in start_urls:
        driver.get(url)

        ciudad = driver.find_element_by_xpath('//h1').text
        current = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]').text
        real_feel = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]').text

        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()

        col.update_one({
            'ciudad': ciudad
        }, {
            '$set': {
                'ciudad': ciudad,
                'current': current,
                'real_feel': real_feel
            }
        }, upsert=True)

        print(ciudad)
        print(current)
        print(real_feel, '\n')
    driver.close()


schedule.every(1).minutes.do(extraer_datos)

while True:
    schedule.run_pending()
    time.sleep(1)