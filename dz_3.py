from bs4 import BeautifulSoup
import requests
from pprint import pprint
import datetime
import time

base_url = "https://habr.com"
url = "https://habr.com/ru/all/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

KEYWORDS = ['JavaScript', 'C++', 'ReactJS', 'python']

list_stat = list()


def decor_link(link_log):
    def decor(old_fuction):
        def new_function(url, keywords, headers):
            result = old_fuction(url, keywords, headers)

            with open(link_log, "a+", encoding="utf-8") as result_file:
                result_file.write(f'Дата и время: {datetime.datetime.now()}' + '\n')
                result_file.write(f'Функция: {old_fuction.__name__}' + '\n')
                result_file.write(f'Аргументы: {url} {keywords} {headers}' + '\n')
                result_file.write(f'Возвращаемый результат: {result}' + '\n')
                result_file.write('\n')

            return result

        return new_function
    return decor


@decor_link('result_function_parse.txt')
def parse_url_tags(url, keywords, headers):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".tm-articles-list")


        for item_pr in container.select('article.tm-articles-list__item'):
            dates = item_pr.select_one(".tm-article-snippet__datetime-published").text
            name = item_pr.select_one(".tm-article-snippet__title-link span").text
            link = base_url + item_pr.select_one(".tm-article-snippet__title-link").attrs["href"]

            list_tag_item_container = item_pr.select_one('.tm-article-snippet__hubs')
            list_tag_item = list()
            for item_tag in list_tag_item_container.select('.tm-article-snippet__hubs-item'):
                list_tag_item.append(item_tag.text.replace(' *', ''))


            result_search = list(set(KEYWORDS) & set(list_tag_item))

            if not result_search:
                pass
            else:
                list_stat.append(dates + ' | ' + name + ' | ' + link)
                print(dates + ' | ' + name + ' | ' + link)

    else:
        print('Ошибка ответа сервера')

    return list_stat

print('Запуск')
parse_url_tags(url, KEYWORDS, headers)
print('Остановка программы')