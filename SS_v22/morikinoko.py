from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep



def get_links(url):
    print('url: {} is starting!'.format(url))
    res = requests.get(url);sleep(2)
    soup = BeautifulSoup(res.text, 'lxml')
    
    titles = soup.select('h1.article-title')
    links = [title.find('a').get('href') for title in titles]
    
    next_link = soup.select_one('li.paging-next').find('a').get('href') if soup.select_one('li.paging-next') is not None else None
    
    return links, next_link


def get_article(links, save_dir):
    for link in links:
        lines, get_lines = list(), list()
        number = os.path.basename(link).split('.')[0]
        print(number);sleep(2)
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        # for i in soup.select("br"):
        #     i.replace_with("\n")
        inner = soup.select_one('div.article-body-inner')
        texts = inner.select('div.mtex')
        if len(texts) == 0:
            texts = inner.select('div.article-body-more')
        for text in texts:
            get_lines.extend(text.get_text('.').split('.'))
        for text in get_lines:
            line = text.replace('\n', '').replace('\u3000', '').replace(' ', '').strip()
            if line != "":
                lines.append(line)
        if lines is not None or lines is not []:
            save_texts(lines, number, save_dir)

def save_texts(texts, number, save_dir):
    save_path = os.path.join(save_dir, number + '.txt')
    with open(save_path, 'w') as f:
        f.write('\n'.join(texts))


def call(save_dir):
    url = 'http://morikinoko.com/?p=726'
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