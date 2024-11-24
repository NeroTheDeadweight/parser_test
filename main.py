import requests
from bs4 import BeautifulSoup
import json


BASE_URL = 'https://quotes.toscrape.com'


def parse_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes_data = []
    quotes = soup.find_all('div', class_='quote')

    # Извлекаем данные из каждой цитаты
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes_data

# Основная функция для сбора данных со всех страниц
def scrape_all_quotes():
    all_quotes = []
    next_page_url = '/page/1/'

    while next_page_url:
        url = BASE_URL + next_page_url
        print(f'Парсинг страницы: {url}')
        quotes = parse_quotes(url)
        all_quotes.extend(quotes)

        # Находим ссылку на следующую страницу
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.find('li', class_='next')
        next_page_url = next_page.a['href'] if next_page else None

    # Записываем данные в JSON-файл
    with open('quotes.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_quotes, json_file, ensure_ascii=False, indent=4)

    print('Данные успешно сохранены в quotes.json')

if __name__ == '__main__':
    scrape_all_quotes()