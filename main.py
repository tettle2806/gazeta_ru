# Парсинг сайтов
# Сбор данных с сайтов - без разрешения
# requests beautifulsoup4


# Парсинг новостного сайта
# Кроме kun.uz   podrobno.uz   bbc.com   gazeta.uz

import requests
from bs4 import BeautifulSoup
import json
html = requests.get('https://lenta.ru/').text
soup = BeautifulSoup(html, 'html.parser')

categories_block = soup.find('ul', class_='menu__nav-list')

categories = categories_block.find_all('li', class_='menu__nav-item')

json_data = []

for category in categories[1:15]:
    category_title = category.find('a').get_text(strip=True) # strip=True убрать лишние пробелы слева справа
    print(category_title)
    category_link = 'https://lenta.ru' + category.find('a').get('href')
    print(category_link)

    json_data.append({
        'category_title': category_title,
        'category_link': category_link,
        'articles': []
    })

    category_page = requests.get(category_link).text
    category_soup = BeautifulSoup(category_page, 'html.parser')

    articles = category_soup.find_all('a', class_='card-big')

    for article in articles:
        article_title = article.find('h3', class_='card-big__title').get_text(strip=True)
        print(article_title)
        try:
            article_description = article.find('span', class_='card-big__rightcol').get_text(strip=True)
        except:
            article_description = 'Нет описания'
        print(article_description)
        article_image = article.find('img').get('src')
        print(article_image)
        try:
            article_time = article.find('time', class_='card-big__date').get_text(strip=True)
        except:
            article_time = 'Время не указано'

        article_link = 'https://lenta.ru' + article.get('href')
        print(article_link)

        json_data[-1]['articles'].append({
            'title': article_title,
            'date': article_time,
            'description': article_description,
            'image': article_image,
            'link': article_link
        })


with open('lenta.json', mode='w', encoding='UTF-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
