# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import re

class YomicomSpider(scrapy.Spider):
    name = 'yomicom'
    allowed_domains = ['yomicom.jp']
    start_urls = ['http://yomicom.jp/']
    page_number = 0

    def parse(self, response):
        links = response.css('div.readmore a::attr(href)').getall()
        for link in links:
            request = scrapy.Request(response.urljoin(link), self.parse_page)
            yield request
        urlbase = self.start_urls[0]
        url = urllib.parse.urljoin(urlbase, 'page-{}.html'.format(self.page_number))
        self.page_number += 1
        request = scrapy.Request(url, callback=self.parse)
        yield request

    def parse_page(self, request):
        url = request.url
        number = url.split('/')[-1].split('-')[-1].strip('.html')
        title = request.css('h2.ently_title a::text').get()
        print('title', title.split('\n')[-1])
        #texts = request.css('div.ently_text div.t_b').xpath('string()').getall()
        texts = request.css('div.ently_text div.t_b::text').getall()
        #Charactor_name (thinking) 「line」
        pattern = '(.*?)[' u'（' u'「' '](.*?)[' u'）' u'」'']'
        cleaned_text = []
        for text in texts:
            text = text.replace(' ', '').replace('\u3000', '').replace('『', '').replace('』', '')
            if text != "":
                line = re.search(pattern, text)
                if line:
                    if line.group(1).strip():
                        cleaned_text.append((line.group(1).strip(),
                                             line.group(2).strip().replace('「', '').replace('」', '').replace('『',
                                                                                                             '').replace(
                                                 '』', '').replace('（', '').replace('）', '').replace('【', '').replace(
                                                 '】', '')))
        if len(cleaned_text) >= 10:
            data = clean_data(cleaned_text)
            with open('yomikomu/{}.txt'.format(number), 'w') as f:
                f.write('\n'.join(data))

def clean_data(texts):
    # 同じ発言者のやつをまとめる。
    # 一人称はわたしに二人称はあなたに置き換えて、三人称は削除する。
    i = 0
    res_text = []
    while True:
        actor = texts[i][0]
        line = texts[i][1]
        while i < len(texts) - 1 and actor == texts[i + 1][0]:
            if not line.endswith('。'):
                if line.endswith('、'):
                    line.rstrip('、')
                line += '。'
            line += texts[i + 1][1]
            i += 1
        res_text.append(actor + ',' + line)
        i += 1
        if i >= len(texts):
            break
    return res_text