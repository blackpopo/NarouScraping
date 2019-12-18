# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum

class HosomikyonuPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.folder = item['folder_name']
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            filename = request._url.rsplit("/", 1)[1]
            path = '{}/{}'.format(self.folder, filename)
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height})
        return checksum
