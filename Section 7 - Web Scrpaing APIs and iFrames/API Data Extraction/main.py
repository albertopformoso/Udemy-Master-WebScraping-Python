import requests
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
           'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=python'}
title = []
num_reviews = []
rating = []

for i in range(1, 4):
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?p=%s&q=python&src=ukw&skip_price=true' % i

    response = requests.get(url_api, headers = headers)

    print(response)

    data = response.json()

    courses = data['courses']

    for course in courses:
        print(course['title'])
        print(course['num_reviews'])
        print(course['rating'], '\n')

        title.append(course['title'])
        num_reviews.append(course['num_reviews'])
        rating.append(course['rating'])

info = {'title': title, 'num_reviews': num_reviews, 'rating': rating}
df = pd.DataFrame(info)
df.to_csv('output.csv')
