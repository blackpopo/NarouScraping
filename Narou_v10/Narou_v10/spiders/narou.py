# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import re
from ..items import NarouV10Item
import os

class NarouSpider(scrapy.Spider):
    name = 'narou'
    params = {
        'genre': '102',
        'order': 'hyoka',
    }
    #allowed_domains = ['yomou.syosetu.com/search.php?genre=101-102']
    # start_urls = ['http://yomou.syosetu.com/search.php?genre=101-102&order=hyoka/']
    start_urls = ['http://yomou.syosetu.com/search.php?{}'.format(urlencode(params))]


    def parse(self, response):
        item = NarouV10Item()
        links = response.css('div.novel_h a::attr(href)').getall()
        for link in links:
            request = scrapy.Request(response.urljoin(link), self.parse_page)
            request.meta['item'] = item
            yield request
        next_page = response.css('div.pager a::attr(href)').getall()[-1]
        # if int(next_page.split('=')[-1]) < 15001:
        #     request = scrapy.Request(response.urljoin(next_page), self.parse)
        #     request.meta['item'] = item
        #     yield request

    def parse_page(self, response):
        item = response.meta['item']
        links = response.css('div.index_box dd.subtitle a::attr(href)').getall()
        title = response.css('p.novel_title::text').get()
        item['title'] = title.replace('\u3000', '')
        author = response.css('div.novel_writername a::text').get()
        if author == None:
            author = response.css('div.novel_writername::text').get()
            author = author.split('：')[-1]
        print(author)
        item['author'] = author.replace('\u3000', '')
        if links:
            for link in links:
                request = scrapy.Request(response.urljoin(link), self.parse_series)
                request.meta['item'] = item
                yield request
        else:
            text = response.css('div#novel_honbun').xpath('string()').get()
            text = self.arrange_text(text)
            discourse = self.extract_discourse(text)
            item['url'] = response.url
            item['subtitle'] = title
            self.write_text(discourse, self.extract_code(response.url))
            #item['discourse'] = discourse
            yield item

    def parse_series(self, response):
        item = response.meta['item']
        item['url'] = response.url
        subtitle = response.css('p.novel_subtitle::text').get()
        item['subtitle'] = subtitle.replace('\u3000', '')
        text = response.css('div#novel_honbun').xpath('string()').get()
        text = self.arrange_text(text)
        discourse = self.extract_discourse(text)
        self.write_text(discourse, self.extract_code(response.url))
        #item['discourse'] = discourse
        yield item

    def arrange_text(self, texts):
        text = texts.replace('\u3000', '').replace('\n', '')
        return text


    def extract_discourse(self, text):
        self.pattern = '「(.*?)」'
        rexp = re.compile(self.pattern)
        result = rexp.findall(text)
        if isinstance(result, str):
            return [result]
        return result

    def write_text(self, texts, code):
        if os.path.exists('./{}.txt'.format(code)):
            with open('./{}.txt'.format(code), 'a') as file:
                file.write('\n'.join(texts) + '\n')
        else:
            with open('./{}.txt'.format(code), 'w') as file:
                file.write('\n'.join(texts) + '\n')

    def extract_code(self, url):
        url_params = url.split('/')
        if url_params[-3].startswith('ncode'):
            return url_params[-2]
        else:
            return url_params[-3]

