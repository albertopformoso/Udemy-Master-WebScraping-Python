from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")

driver = webdriver.Chrome(chrome_options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:
    captcha_key = driver.find_element_by_id('recaptcha-demo').get_attribute('data-sitekey')

    url = "https://2captcha.com/in.php?"
    url += "key=" + "f300d3f245f9820efaced256a2b5c942"  # API KEY 2CAPTCHA
    url += "&method=userrecaptcha"
    url += "&googlekey=" + captcha_key
    url += "&pageurl=" + url
    url += "&json=0"

    print(url)

    respuesta_requerimiento = requests.get(url)

    captcha_service_key = respuesta_requerimiento.text

    print(captcha_service_key)

    captcha_service_key = captcha_service_key.split('|')[-1]

    url_resp = "https://2captcha.com/res.php?"
    url_resp += "key=" + "f300d3f245f9820efaced256a2b5c942"  # API KEY
    url_resp += "&action=get"
    url_resp += "&id=" + captcha_service_key  # ID del captcha en el sistema de 2CAPTCHA obtenido previamente
    url_resp += "&json=0"

    print(url_resp)

    sleep(20)

    while True:
        respuesta_solver = requests.get(url_resp)
        respuesta_solver = respuesta_solver.text
        print(respuesta_solver)

        if respuesta_solver == "CAPCHA_NOT_READY":
            sleep(5)

        else:
            break

    respuesta_solver = respuesta_solver.split('|')[-1]
    print()

    insertar_solucion = 'document.getElementById("g-recaptcha-response").innerHTML="' + respuesta_solver + '";'
    print(insertar_solucion)


    driver.execute_script(insertar_solucion)


    submit_button = driver.find_element_by_xpath('//input[@id="recaptcha-demo-submit"]')
    submit_button.click()
except Exception as e:
    print(e)


print("Ya debo de estar en la pagina donde esta la informacion...")

contenido = driver.find_element_by_class_name('recaptcha-success')
print(contenido.text)