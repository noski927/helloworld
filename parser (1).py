import requests
from bs4 import BeautifulSoup
import csv
import time


with open('herbar.csv')as data:
    herbarium = data.read()
herb = herbarium.split(sep='\n')
del (herb[-1])
data_all = []

URL = 'http://herbarium.nrm.se/specimens/S17-38024'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0',
           'accept': '*/*'}
HOST = 'https://herbarium.nrm.se/'
FILE = 'herb.csv'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='inner')
    data = []
    for item in items:
        data.append(
            item.find('div', class_='col-sm-9').get_text()
        )
    return (data)


def save_file(items, path):
    with open(path, 'w', newline='\n', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Registration number', 'Collector', 'Collector number', 'Collection date', 'Label Information',
                         'Coordinates', 'Determinations', 'Family'])
        for line in items:
            writer.writerow(line)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        data = []
        for page in herb:
            html = get_html(page)
            data.append(get_content(html.text))
            #time.sleep(3)
            print(f'Парсинг страницы {page} из многа...')
        for i in data:
            del(i[-1])
        print(data)
        save_file(data, FILE)

    else:
        print('err')


parse()