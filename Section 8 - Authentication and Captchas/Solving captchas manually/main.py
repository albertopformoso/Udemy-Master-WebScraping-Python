from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')

driver = webdriver.Chrome('../chromedriver.exe',options=opts)

url = 'http://google.com/recaptcha/api2/demo'
driver.get(url)

try:
    driver.switch_to.frame(driver.find_element_by_xpath('//iframe'))
    captcha = driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-border"]')
    captcha.click()

    input()

    driver.switch_to.default_content()
    submit = driver.find_element_by_xpath('//*[@id="recaptcha-demo-submit"]')
    submit.click()

except:
    print('error')

content = driver.find_element_by_class_name('recaptcha-success').text
print(content)
