from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

driver.get('https://www.olx.com.ec/')
driver.maximize_window()

for i in range(3):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # Button Click "Cargar mas"
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
    except:
        pass

# All the ads in a list
ads = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

for ad in ads:
    price = ad.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    description = ad.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text

    print(price, description)
