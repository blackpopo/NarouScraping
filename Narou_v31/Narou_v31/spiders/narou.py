# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import re

from scrapy.crawler import CrawlerProcess

import os

class NarouSpider(scrapy.Spider):
    name = 'narou'
    # params_list = [{
    #     'genre': '102',
    #     'order': 'hyoka',
    # },              {
    #     'genre': '9903',
    #     'order': 'hyoka'
    # },      {
    #     'genre': '302',
    #     'order': 'hyoka'}
    # ]
    
    def __init__(self, genre):
        super(NarouSpider, self).__init__()
        params = {'genre': str(genre), 'order': 'hyoka'}
        self.start_urls = ['http://yomou.syosetu.com/search.php?{}'.format(urlencode(params))]
        self.genre_dict = {
            '102': 'Modern_Renai',
            '9903': 'Essay',
            '302': 'Non_Genre'
        }

    def parse(self, response):
        genre = re.compile('genre=(\d+)')
        page_lines = response.css('div.novel_h a::attr(href)').getall()
        self.genre = self.genre_dict[genre.search(response.url).group(1)]
        for page in page_lines:
            # print('Title Links ', page)
            request = scrapy.Request(page, callback=self.parse_subtile_page)
            yield request
        next_page = response.css('div.pager a::attr(href)').get()
        if next_page:
            request = scrapy.Request(response.urljoin(next_page), callback=self.parse)
            yield request
    
    def parse_subtile_page(self, response):
        next_links = response.css('dd.subtitle a::attr(href)').getall()
        if next_links is None:
            request = scrapy.Request(response.url, callback=self.parse_page)
            yield request
        else:
            for link in next_links:
                # print('Subtitle Links ', response.urljoin(link))
                request = scrapy.Request(response.urljoin(link), callback=self.parse_page)
                yield request
            
    def parse_page(self, response):
        code = re.compile('https://ncode.syosetu.com/(.*?)/.*?')
        self.code = code.search(response.url).group(1)
        text = response.css('div#novel_honbun').xpath('string()').extract_first()
        text = text.split('\n')
        text = [tx.strip() for tx in text if tx.replace('\n', '').strip() != '']
        with open(os.path.join('/ssd/Narou', self.genre, self.code + '.txt'), 'a') as f:
            f.write('\n'.join(text))
            
# process = CrawlerProcess()
# process.crawl(NarouSpider, genre='102')
# process.crawl(NarouSpider, genre='9903')
# process.crawl(NarouSpider, genre='302')
# process.start()