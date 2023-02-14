from requests import *
import base_updater

updater = base_updater.Updater()

from bs4 import BeautifulSoup

import dict

dictonary = dict.Dictionary()

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/92.0.4515.159 Safari/537.36', 'accept': '*/*', "connection": "keep-alive"}


pars_url = 'https://animestars.org/'
page_num = '/page/'


def get_page_num(page, page_n):
    if page != 1:
        page_n += str(page) + '/'
    else:
        page_n = ""
    return page_n


def get_html(url, headers, params=None):
    r = get(url, headers=headers, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_='rels-shot short clearfix')
    return items


def get_names(items):
    names = []
    item1 = items.find_all('div', class_='short-text')
    for item in item1:
        names.append(item.find('a', class_='short-t').text)
    return names


def get_cards():
    items = []
    for page in range(57):
        html = get_html(pars_url + get_page_num(page + 1, page_num), HEADERS)
        if html.status_code == 200:
            items.append(get_content(html.text))
        else:
            return "Error"
    return items


def get_hrefs(items):
    hrefs = []
    item1 = items.find_all('div', class_='short-text')
    for item in item1:
        hrefs.append(item.find('a', class_='short-t').get('href'))
    return hrefs


def get_genres(href):
    genres = []
    html = get_html(href, HEADERS)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='fi-col-item')
    for item in items:
        row_name = item.find('div', class_='sfull-t').text
        if row_name == "Жанр":
            for genre in item.find_all('a'):
                genres.append(genre.text)
    return genres


def parse():
    items = get_cards()
    i = 0
    animes = []
    for item in items:
        for card in item:
            href = get_hrefs(card)[0]
            animes.append({
                'name' + str(i):  get_names(card),
                'href' + str(i): href,
                'genres' + str(i): get_genres(href)
            })
            i += 1
    dictonary.animes = animes
    updater.update(dictonary.animes)


parse()
