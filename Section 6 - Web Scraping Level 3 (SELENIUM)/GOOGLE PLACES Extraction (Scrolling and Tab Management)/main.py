import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

scrollingScript = """ 
document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 20000)
"""

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')

driver = webdriver.Chrome(options=opts)

driver.get(
    'https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1')

sleep(random.uniform(4.0, 5.0))

SCROLLS = 0
while SCROLLS != 3:
    driver.execute_script(scrollingScript)
    sleep(random.uniform(5, 6))
    SCROLLS += 1

reviews_restaurant = driver.find_elements(By.XPATH, '//div[contains(@class,"section-review ripple-container")]')

for review in reviews_restaurant:
    userLink = review.find_element(By.XPATH, './/div[@class="section-review-title"]')

    try:
        userLink.click()
        driver.switch_to.window(driver.window_handles[1])

        opiniones_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="section-tab-bar-tab ripple-container section-tab-bar-tab-unselected"]'))
        )
        opiniones_tab.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="section-layout section-scrollbox scrollable-y scrollable-show"]'))
        )

        USER_SCROLLS = 0
        while USER_SCROLLS != 3:
            driver.execute_script(scrollingScript)
            USER_SCROLLS += 1

        user_reviews = driver.find_elements_by_xpath('//div[contains(@class,"section-review ripple-container")]')

        for userReview in user_reviews:
            reviewRating = userReview.find_element(By.XPATH, './/span[@class="section-review-stars"]').get_attribute(
                'aria-label')
            userParsedRating = float(''.join(filter(str.isdigit or str.isspace, reviewRating)))
            reviewText = userReview.find_element(By.XPATH, './/span[@class="section-review-text"]').text

            print(userParsedRating)
            print(reviewText)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(e, 'error')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
