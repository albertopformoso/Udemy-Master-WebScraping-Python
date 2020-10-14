import requests
import json

headers = {'user-agent': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

endpoint = 'https://api.github.com/user/repos'

user = 'XXX'
password = 'XXX'

response = requests.get(endpoint, headers=headers, auth=(user, password))

repos = response.json()

for repo in repos:
    print(repo['name'], '\n')