import selenium
from selenium.webdriver import Chrome

from bs4 import BeautifulSoup
import requests
import os
import re
from time import sleep
from SS_processor import process_text

#Titleを取得
def get_links(url, driver):
    print('url: {} is starting!'.format(url))
    driver.get(url)
    sleep(5)
    titles = driver.find_elements_by_css_selector('div.main_section_head_sbu')

    links = [title.find_element_by_css_selector('h2').get_attribute('href') for title in titles]
    
    next_link = None
    
    return links, next_link

#link先から文章の取得
def get_article(links, save_dir, url_str, driver):
    for link in links:
        lines = list()
        link = url_str.rstrip('/') + link
        number = os.path.basename(link).split('.')[0]
        print(number);
        driver.get(link)
        source = driver.Page_source
        soup = BeautifulSoup(source, 'lxml')
        inner = soup.select_one('div#main_sction_body')
        texts = inner.select('dd.t_b')
        for text in texts:
            lines.extend(text.get_text('.').split('.'))
        print(lines)
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
    driver = Chrome('/home/maya/anaconda3/lib/python3.7/site-packages/chromedriver_binary/chromedriver')
    url_str = 'http://ss-navi.com/page-{}.html'
    for i in range(1100):
        url = url_str.format(i)
        links, next_link = get_links(url, driver)
        print(links)
        get_article(links, save_dir, url_str, driver)

if __name__=='__main__':
    save_dir = 'test_dir'
    call(save_dir)