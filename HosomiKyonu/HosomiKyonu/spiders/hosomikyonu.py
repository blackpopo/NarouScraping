# -*- coding: utf-8 -*-
import scrapy
import requests
from ..items import HosomikyonuItem
import time
from selenium.webdriver import Chrome, ChromeOptions
import chromedriver_binary
from bs4 import BeautifulSoup
import random

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST)}

class HosomikyonuSpider(scrapy.Spider):
    name = 'hosomikyonu'
    # allowed_domains = ['twitter.com/hosomikyonyu']
    start_urls = ['http://twitter.com/j5yyklx4n54euwr']

    # def start_requests(self):
    #     with open('link_urls.txt') as f:
    #         params = {
    #             'session[username_or_email]': 'KayaTakashiro',
    #             'session[password]': 'mayal0ve'
    #         }
    #         for link in f:
    #             yield scrapy.FormRequest(link, callback=self.parse, method='POST', formdata=params)

    def start_requests(self):
        yield scrapy.Request('http://twitter.com/Japanese_OPPAI', callback=self.parse, headers=HEADER)

    def parse(self, response):
        item = HosomikyonuItem()
        item['folder_name'] = response.url.rsplit("/", 1)[1]
        print(item['folder_name'])
        item['image_urls'] = []
        delay_sec = 1.0

        options = ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('--headless')
        driver = Chrome(options=options)
        print(response.url)
        driver.get(response.url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # stream_end = driver.find_element_by_css_selector(
            #     "div.content > div.stream-item-footer")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay_sec)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if  last_height == new_height:
                break
            last_height = new_height
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tweets = soup.find_all('div', {'class': 'tweet'})
        for tweet in tweets:
            images = tweet.find_all('div', attrs={'class': 'AdaptiveMedia-photoContainer'})
            for image in images:
                url = image.get('data-image-url')
                item['image_urls'].append(url)

        # tweets = soup.find_all('div', {'class': 'r-1p0dtai'})
        # print(tweets)
        # for tweet in tweets:
        #     images = tweet.find_all('img')
        #     for image in images:
        #         url = image.get('src')
        #         item['image_urls'].append(url)

        print(item['folder_name'], 'is_finished')
        return item




        # urls = response.css('div.tweet div.AdaptiveMedia-photoContainer::attr(data-image-url)').extract()
        # print(len(urls))
        # for url in urls:
        #     print(url)
        # request = scrapy.Request(response.urljoin(next_page), self.parse)
        # yield item
            # buttons = driver.find_elements_by_class_name('AdaptiveMediaOuterContainer')
            # for button in buttons:
            #     display = button.find_element_by_class_name('Tombstone-action')
            #     display.click()
        # items = driver.find_elements_by_class_name('content')
        # for item in items:
        #     urls = item.find_elements_by_class_name('AdaptiveMedia-photoContainer')
        #     for url in urls:
        #         img_url = url.find_element_by_css_selector('img').get_attribute('src')
        #         print(img_url)
        urls = []
