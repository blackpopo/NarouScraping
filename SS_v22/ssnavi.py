from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep



#Titleを取得
def get_links(url):
    print('url: {} is starting!'.format(url))
    res = requests.get(url);sleep(2)
    soup = BeautifulSoup(res.text, 'lxml')
    
    titles = soup.select('div.main_section_head_sbu')
    links = [title.find('a').get('href') for title in titles]
    
    next_link = None
    
    return links, next_link

#link先から文章の取得
def get_article(links, save_dir, url_str):
    for link in links:
        lines, get_lines = list(), list()
        link = url_str.rstrip('/') + link
        number = os.path.basename(link).split('.')[0]
        print(number);sleep(2)
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'lxml')
        print(soup.find('div'))
        inner = soup.find('div', id='main_section_body')
        texts = inner.select('dd.t_b', id='main_section_body')
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
    url_str = 'http://ss-navi.com/page-{}.html'
    for i in range(1, 1100):
        url = url_str.format(i)
        links, next_link = get_links(url)
        
        
        get_article(links, save_dir, url_str)

if __name__ == '__main__':
    save_dir = 'test_dir'
    call(save_dir)