import requests
from PIL import Image  # pip install Pillow
import io
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec')

for i in range(1):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )

    except:
        break

driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)

driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)

ads = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

i = 0

for ad in ads:
    print(ad.get_attribute('innerHTML'))

    price = ad.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print(price)

    description = ad.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print(description)

    try:
        url = ad.find_element_by_xpath('.//figure[@data-aut-id="itemImage"]/img')

        url = url.get_attribute('src')

        image_content = requests.get(url).content

        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = 'images/' + str(i) + '.jpg'
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
    except Exception as e:
        print(e)
        print("Error")
    i += 1
