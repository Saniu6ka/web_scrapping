import requests
import bs4
import fake_headers
from urllib.parse import urljoin

def process_article(article_tag, keywords):
    time_tag = article_tag.find('time')
    pub_time = time_tag['datetime']

    h2_tag = article_tag.find('h2', class_='tm-title')
    span_tag = h2_tag.find('span')

    header = span_tag.text.strip()

    a_tag = h2_tag.find('a')
    link_relative = a_tag['href']

    link_absolute = urljoin("https://habr.com/", link_relative)

    response = requests.get(link_absolute, headers=headers_gen.generate())
    article_html_data = response.text
    article_soup = bs4.BeautifulSoup(article_html_data, "html5lib")

    # получение блока с текстом статьи
    article_text = article_soup.find('div', class_='tm-article-body').get_text(strip=True, separator=' ')

    # проверка содержания ключевых слов в статье
    if any(keyword.lower() in article_text.lower() for keyword in keywords):
        return {
            'header': header,
            'link': link_absolute,
            'pub_time': pub_time
        }
    return None


# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

headers_gen = fake_headers.Headers(os="win", browser="chrome")

HOST = 'https://habr.com/ru/articles/'

response = requests.get(HOST, headers=headers_gen.generate())
main_htm_data = response.text
main_soup = bs4.BeautifulSoup(main_htm_data, 'lxml')

articles_list_tag = main_soup.find(name='div', class_='tm-articles-list')

article_tags = articles_list_tag.find_all('article')
articles_data = []

for article_tag in article_tags:
    result = process_article(article_tag, KEYWORDS)
    if result:
        articles_data.append(result)

# вывод информации
for article in articles_data:
    print(f"{article['pub_time']} - {article['header']} - {article['link']}")