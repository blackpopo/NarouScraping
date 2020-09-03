# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import pickle

import spacy


ginza = spacy.load('ja_ginza')

class SshoukoSpider(scrapy.Spider):
    name = 'sshouko'
    allowed_domains = ['sshouko.net']
    start_urls = ['http://sshouko.net/page-0.html']


    def parse(self, response):
        next_links = response.css('h2.entry-header > a::attr(href)').getall()
        for link in next_links:
            yield Request(link, callback=self.parse_page)
        number = response.url.split('/')[-1].split('-')[-1].strip('.html')
        next_page = response.url.replace(number, str(int(number)+1))
        try:
            yield Request(next_page, callback=self.parse)
        except:
            pass

    def parse_page(self, response):
        url = response.url
        number = url.split('/')[-1].split('-')[-1].strip('.html')
        title = response.css('h2.entry-header > a::text').get()
        print('title', title.split('\n')[-1])
        texts = response.css('div.t_b::text').getall()
        pattern = '(.*?)[' u'（' u'「' '](.*?)[' u'）' u'」'']'
        cleaned_text = []
        for text in texts:
            text = text.replace(' ', '').replace('\u3000', '').replace('『', '').replace('』', '')
            if text != "":
                line = re.search(pattern, text)
                if line:
                    if line.group(1).strip():
                        cleaned_text.append((line.group(1).strip(), line.group(2).strip().replace('「', '').replace('」', '').replace('『', '').replace('』', '').replace('（', '').replace('）', '').replace('【', '').replace('】', '')))
        if len(cleaned_text) >= 10:
            data = clean_data(cleaned_text)
            with open('sshouko/{}.txt'.format(number), 'w') as f:
                f.write('\n'.join(data))


def clean_data(texts):
    #同じ発言者のやつをまとめる。
    #一人称はわたしに二人称はあなたに置き換えて、三人称は削除する。
    i = 0
    res_text = []
    while True:
        actor = texts[i][0]
        line = texts[i][1]
        while  i < len(texts)-1 and actor == texts[i+1][0]:
            if not line.endswith('。'):
                if line.endswith('、'):
                    line.rstrip('、')
                line += '。'
            line += texts[i+1][1]
            i += 1
        res_text.append(actor + ',' + line)
        i += 1
        if i >= len(texts):
            break
    return res_text



