import schedule
import time
from selenium import webdriver

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]


def data_extractor():
    driver = webdriver.Chrome()

    for url in start_urls:
        driver.get(url)
        time.sleep(5)

        city: object = driver.find_element_by_xpath('//h1').text
        current = driver.find_element_by_xpath(
            '/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[1]').text
        real_feel = driver.find_element_by_xpath(
            '/html/body/div/div[5]/div[1]/div[1]/a[1]/div[1]/div[1]/div/div/div[2]').text

        city = city.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()

        f = open("datos_clima_selenium.csv", "a")
        f.write(city + "," + current + "," + real_feel + "\n")
        f.close()
        print(city)
        print(current)
        print(real_feel)
        print()

    driver.close()


schedule.every(1).minutes.do(data_extractor)

while True:
    schedule.run_pending()
    time.sleep(1)
