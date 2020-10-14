import requests
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter('ignore')

seed_url = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/"

resp = requests.get(seed_url)
print(resp)
soup = BeautifulSoup(resp.text)

urls = []

downloads = soup.find_all('a', class_="download-button")
for download in downloads:
    urls.append(download["href"])

i = 0
for url in urls:
    r = requests.get(url, allow_redirects=True)
    file_name = 'files/excel-file-' + str(i) + '.xls'
    output = open(file_name, 'wb')
    output.write(r.content)
    output.close()
    i += 1
