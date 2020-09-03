from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep



def get_links(url):
    print('url: {} is starting!'.format(url))
    res = requests.get(url);sleep(2)
    soup = BeautifulSoup(res.text, 'html5lib')
    
    titles = soup.select('div.article')
    links = [title.find('a').get('href') for title in titles]
    
    next_link = soup.select_one('li.paging-next').find('a').get('href') if soup.select_one('li.paging-next') is not None else None
    
    return links, next_link


def get_article(links, save_dir):
    for link in links:
        lines, get_lines = list(), list()
        number = os.path.basename(link).split('.')[0]
        print(number);sleep(2)
        res = requests.request('get',link)
        soup = BeautifulSoup(res.text, 'html5lib')
        inner = soup.select_one('div.article')
        texts = inner.select('dd')
        texts2 = inner.find_all('font', color='#ed1c24')
        texts3 = inner.select('dt')
        if texts == [] and texts2 == []:
            for span in inner('span'):
                span.decompose()
            for div in inner('div'):
                div.decompose()
            for ul in inner('ul'):
                ul.decompose()
            for font in inner('font'):
                font.decompose()
            # print(inner)
            get_lines = inner.get_text('.').split('.')
        elif  texts2 != []:
            # print(texts, texts2)
            for text in texts2:
                get_lines.extend(text.get_text('.').split('.'))
        elif texts3 != []:
            for text in texts3:
                get_lines.extend(text.get_text('.').split('.'))
        else:
            # print(texts)
            for text in texts:
                get_lines.extend(text.get_text('.').split('.'))
        for text in get_lines:
            line = text.replace('\n', '').replace('\u3000', '').replace(' ', '').strip()
            if line != "":
                lines.append(line)
        if lines is not [] or lines is not None:
            save_texts(lines, number, save_dir)


def save_texts(texts, number, save_dir):
    save_path = os.path.join(save_dir, number + '.txt')
    with open(save_path, 'w') as f:
        f.write('\n'.join(texts))


def call(save_dir):
    url = 'http://elephant.2chblog.jp/?p=2700'
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