from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

client = MongoClient('localhost')
db = client['olx']
col = db['anuncios_selenium']

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec')

for i in range(3):
    try:

        boton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

        boton.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )

    except Exception as e:
        print(e)

        break

driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)

autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

for auto in autos:

    try:
        precio = auto.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    except:
        precio = 'NO DISPONIBLE'

    descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text

    col.insert_one({
        'precio': precio,
        'descripcion': descripcion
    })
