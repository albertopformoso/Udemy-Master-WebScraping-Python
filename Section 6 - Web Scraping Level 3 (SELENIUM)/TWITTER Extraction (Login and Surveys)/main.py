import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')

driver = webdriver.Chrome(options=opts)

user = "XXX"
password = 'XXX'

driver.get('https://twitter.com/login')

input_user = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input')
input_pass = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input')

input_user.send_keys(user)
input_pass.send_keys(password)

# Login button click
driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div').click()

tweets = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//section//article//div[@dir="auto"]'))
)

for tweet in tweets:
    print(tweet.text)