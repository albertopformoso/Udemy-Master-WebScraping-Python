import requests
import pandas as pd

headers = {'user-agent': 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
           'referer': 'https://www.udemy.com/courses/search/?src=ukw&q=python'}

all_courses = []

for i in range(1, 4):
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?p=%s&q=python&src=ukw&skip_price=true' % i

    response = requests.get(url_api, headers = headers)

    # print(response)

    data = response.json()

    courses = data['courses']

    for course in courses:
        all_courses.append({'title': course['title'],
                            'rating': course['rating'],
                            'num_reviews': course['num_reviews']})

df = pd.DataFrame(all_courses)

print(df)

df.to_csv('udemy_python_courses.csv')
