import requests
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter('ignore')

headers = {
    'user-agent': "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
}

url = 'https://stackoverflow.com/questions'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text)

questions_container = soup.find(id='questions')
questions_list = questions_container.findAll('div', class_='question-summary')
# Option 2
# questions_list = questions_container.findAll('div', {'class': 'question-summary'})

for question in questions_list:
    # Extract question title
    question_text = question.find('h3').text

    # Extract question description
    question_description = question.find(class_='excerpt').text
    question_description = question_description.replace('\n', '').replace('\r', '').strip()

    print(question_text)
    print(question_description + '\n')

# Option 2
# for question in questions_list:
#     # Extract question title
#     element_question_text = question.find('h3')
#     question_text = element_question_text.text
#
#     # Extract question description
#     question_description = element_question_text.find_next_sibling('div').text
#     question_description = question_description.replace('\n', '').replace('\r', '').strip()
#
#     print(question_text)
#     print(question_description + '\n')