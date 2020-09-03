import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin
import sys
from time import sleep
import random

user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3864.0 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:68.0) Gecko/20100101 Firefox/68.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
               ]

def main():
    genre = sys.argv[1]
    assert genre=='102' or genre=='9903' or genre=='302', 'Genre Error :{}\n' \
                                                          ' Select from 102, 9903, 302!'.format(genre)
    genre_dict = {
        '102': 'Modern_Renai',
        '9903': 'Essay',
        '302': 'Non_Genre'
    }

    for i in range(1, 101):
        params = {'genre': genre, 'order': 'hyoka', 'p': str(i)}
        url = 'http://yomou.syosetu.com/search.php?{}'.format(urlencode(params))
        print('url {} is starting'.format(url))
        parse_title_page(url, genre_dict[genre])

    
def parse_title_page(url, genre):
    user_agent = random.choice(user_agents)
    response = requests.get(url, headers={'User-Agent': user_agent})
    sleep(0.5)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = soup.select('div.novel_h')
    title_links = [title.find('a').get('href') for title in titles]
    for title_link in title_links:
        # print('Title Link', title_link)
        parse_subtitle_page(title_link, genre)
    # next_page = soup.select_one('div.pager')
    # if next_page is not None:
    #     next_page = next_page.find('a').get('href')
    #     next_page = urljoin(response.url, next_page)
    #     print('Next Page', next_page)
    #     parse_title_page(next_page, genre)
        
def parse_subtitle_page(url, genre):
    user_agent = random.choice(user_agents)
    response = requests.get(url, headers={'User-Agent': user_agent})
    sleep(0.5)
    soup = BeautifulSoup(response.text, 'lxml')
    sub_title_links = soup.select('dd.subtitle')
    if sub_title_links == []:
        print(url)
        parse_page(url, genre)
    # else:
    #     sub_title_links = [subtitle.find('a').get('href') for subtitle in sub_title_links]
    #     for sub_title_link in sub_title_links:
    #         link = urljoin(response.url, sub_title_link)
    #         # print('Subtitle_Link', link)
    #         parse_page(link, genre)

def parse_page(url, genre):
    user_agent = random.choice(user_agents)
    try:
        response = requests.get(url, headers={'User-Agent': user_agent})
        sleep(0.1)
        soup = BeautifulSoup(response.text.encode('utf-8'), 'lxml')
        re_code = re.compile('https://ncode.syosetu.com/(.*?)/.*?')
        sub_title = soup.select_one('p.novel_subtitle')
        if sub_title is not None:
            sub_title = soup.select_one('p.novel_subtitle').text
        else:
            sub_title = ''
        if '登場人物' not in sub_title and '設定' not in sub_title and '資料' not in sub_title and not'人物紹介' in sub_title:
            code = re_code.search(url).group(1)
            text = soup.select_one('div#novel_honbun').text
            text = text.split('\n')
            text = [tx.strip() for tx in text if tx.replace('\n', '').strip() != '']
            with open(os.path.join('/ssd/Narou', genre + '_Tanpen' , code + '.txt'), 'a') as f:
                f.write('\n'.join(text))
            print('parse {}'.format(url))
        else:
            # print(sub_title)
            pass
    except Exception as err:
        print(err)
        parse_page(url, genre)
    
if __name__=='__main__':
    main()