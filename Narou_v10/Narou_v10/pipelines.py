# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
from scrapy.exporters import JsonLinesItemExporter

class NarouV10Pipeline(object):

    def open_spider(self, spider):
        self.url_exporter = {}

    def close_spider(self, spider):
        for exporter in self.url_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_items(self, item):
        url = item['url'].split('/')
        if url[-3].startswith('n'):
            code = url[-3]
        else:
            code = url[-2]
        if code not in self.url_exporter:
            file = open('{}.jl'.format(code), 'wb')
        else:
            file = open('', 'ab')
        exporter = JsonLinesItemExporter(file)
        exporter.start_exporting()
        self.url_exporter[code] = exporter
        return self.url_exporter[code]

    def process_item(self, item, spider):
        exporter = self._exporter_for_items(item)
        exporter.export_item(item)
        return item
