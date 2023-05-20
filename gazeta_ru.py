import json

import requests
from bs4 import BeautifulSoup

html = requests.get('https://www.gazeta.ru/').text
soup = BeautifulSoup(html, 'html.parser')

categories_block = soup.find('div', class_='b_menu-content')

categories = categories_block.find_all('div', class_='b_menu-item')

json_data = []

for category in categories[:11]:
    categorie_title = category.find('a').get_text(strip=True)
    print(categorie_title)
    category_link = 'https://www.gazeta.ru' + category.find('a').get('href')
    print(category_link)

    json_data.append({
        'Category_Title': categorie_title,
        'Category_Link': category_link,
        'Articles': []
    })

    category_page = requests.get(category_link).text
    category_soup = BeautifulSoup(category_page, 'html.parser')

    articles = category_soup.find_all('div', class_='w_col1')

    for article in articles:
        try:
            article_title = article.find('div', class_='b_ear-title').get_text(strip=True)
            print(article_title)
        except:
            article_title = 'Нет Описания'
            print(article_title)

        try:
            article_description = article.find('div', class_='b_ear-intro').get_text(strip=True)
            print(article_description)
        except:
            article_description = 'Нету Описания'
            print(article_description)

        try:
            article_img = article.find('img').get('src')
            print(article_img)
        except:
            article_img = 'Статья не имеет фотографии'
            print(article_img)

        try:
            article_time = article.find('time').get_text(strip=True)
            print(article_time)
        except:
            article_time = 'Время не задано'
            print(article_time)

        try:
            article_link = 'https://www.gazeta.ru' + article.find('a').get('href')
            print(article_link)
        except:
            article_link = 'Ссылка не доступна'
            print(article_link)

        json_data[-1]['Articles'].append({
            'Title': article_title,
            'Date': article_time,
            'Description': article_description,
            'Image': article_img,
            'Link': article_link
        })


with open('gazeta_ru.json', mode='w', encoding='UTF-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)