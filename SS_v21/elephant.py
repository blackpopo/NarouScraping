from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep
from SS_processor import process_text


def get_links(url):
    print('url: {} is starting!'.format(url))
    res = requests.request('get', url);sleep(2)
    soup = BeautifulSoup(res.text, 'html5lib')
    # print(soup)
    titles = soup.find_all('div', class_='article')
    links = [title.find('h2').find('a').get('href') for title in titles]
    print(links)
    next_link = soup.select_one('li.paging-next').find('a').get('href') if soup.select_one('li.paging-next') else None
    return links, next_link


def get_article(links, save_dir):
    for link in links:
        lines = list()
        number = os.path.basename(link).split('.')[0]
        print(number);sleep(2)
        res = requests.request('get',link)
        soup = BeautifulSoup(res.text, 'html5lib')
        inner = soup.select_one('div.article')
        texts = inner.select('dd')
        texts2 = inner.find_all('font', color='#ed1c24')
        texts3 = inner.select('dt')
        if texts == [] and texts2 == []:
            print('texts0')
            for span in inner('span'):
                span.decompose()
            for div in inner('div'):
                div.decompose()
            for ul in inner('ul'):
                ul.decompose()
            for font in inner('font'):
                font.decompose()
            # print(inner)
            lines = inner.get_text('.').split('.')
        elif  texts2 != []:
            print('texts2')
            # print(texts, texts2)
            for text in texts2:
                lines.extend(text.get_text('.').split('.'))
        elif texts3 != []:
            print('texts3')
            for text in texts3:
                lines.extend(text.get_text('.').split('.'))
        else:
            print('texts1')
            # print(texts)
            for text in texts:
                lines.extend(text.get_text('.').split('.'))
        texts = process_text(lines)
        if texts is not None:
            save_texts(texts, number, save_dir)

def save_texts(texts, number, save_dir):
    existed_files = os.listdir(save_dir)
    save_path = os.path.join(save_dir, number + '.txt')
    if not save_path in existed_files:
        with open(save_path, 'w') as f:
            f.write('\n'.join(texts))


def call(save_dir):
    url = 'http://elephant.2chblog.jp/?p=4207'
    while True:
        links, next_link = get_links(url)
        
        get_article(links, save_dir)
        if next_link is not None:
            url = next_link
        else:
            break


if __name__ == '__main__':
    save_dir = 'test_dir'
    call(save_dir)
