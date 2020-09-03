# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re


class EsusokuhouSpider(scrapy.Spider):
    name = 'esusokuhou'
    #allowed_domains = ['esusokuhou.blog.jp']
    start_urls = ['http://esusokuhou.blog.jp/']

    def parse(self, response):
        links = response.css('h1.article-title > a::attr(href)').getall()
        for link in links:
            request = Request(link, callback=self.parse_page)
            yield request
        next_page_link = response.css('div.nextpage li.paging-next > a::attr(href)').get()
        if next_page_link:
            request = Request(next_page_link, callback=self.parse)
            yield request

    def parse_page(self, response):
        title = response.css('h1.article-title a::text').get()
        print(title)
        number = response.url.rsplit('/', 1)[-1].split('.')[0]
        texts = response.css('div.t_b::text').getall()
        pattern = '(.*?)[' u'（' u'「' '](.*?)[' u'）' u'」'']'
        cleaned_text = []
        for text in texts:
            text = text.replace(' ', '').replace('\u3000', '').replace('『', '').replace('』', '')
            if text != "":
                line = re.search(pattern, text)
                if line:
                    if line.group(1).strip():
                        cleaned_text.append((line.group(1).strip(),
                                             line.group(2).strip().replace('「', '').replace('」', '').replace('『','').replace(
                                                 '』', '').replace('（', '').replace('）', '').replace('【', '').replace(
                                                 '】', '')))
        if len(cleaned_text) >= 10:
            data = clean_data(cleaned_text)
            with open('esusokuhou/{}.txt'.format(number), 'w') as f:
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
