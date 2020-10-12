import random
from time import sleep
from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec/autos_c378')
driver.maximize_window()

# button = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')

for i in range(3):
    try:
        # Button Click "Cargar mas"
        driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]').click()
        sleep(random.uniform(8.0, 10.0))
    except:
        pass

# All the ads in a list
cars = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

for car in cars:
    price = car.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    description = car.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text

    print(price, description)
