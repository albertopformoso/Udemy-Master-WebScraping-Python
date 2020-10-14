from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0')

driver = webdriver.Chrome(options=opts)