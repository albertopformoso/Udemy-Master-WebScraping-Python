from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')

driver = webdriver.Chrome(options=opts)

driver.get('https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias')
# driver.maximize_window()

while True:
    product_links = driver.find_elements(By.XPATH, '//a[contains(@class, "ui-search-item")]')
    page_links = []

    for a_tag in product_links:
        page_links.append(a_tag.get_attribute('href'))

    for link in page_links:
        try:
            driver.get(link)
            title = driver.find_element_by_xpath('//*[@id="short-desc"]/div/header/h1').text
            price = driver.find_element_by_xpath('//*[@id="productInfo"]/fieldset[1]/span/span[2]').text
            print(title)
            print(price)
            driver.back()
        except Exception as e:
            print(e)
            driver.back()
            pass
    try:
        next = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        next.click()
    except:
        print('Next Button Error')
        break