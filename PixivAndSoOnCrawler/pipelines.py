# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.request import Request
from itemadapter import ItemAdapter
from PixivAndSoOnCrawler.items import DataItem, ImageItem
from PixivAndSoOnCrawler.settings import *


class PixivandsooncrawlerPipeline:
    def process_item(self, item, spider):
        if isinstance(item, DataItem):
            path = SAVE_DIR
            if ONE_KEYWORD_ONE_DIR:
                if not os.path.isdir(os.path.join(path, item['keyword'])):
                    os.mkdir(os.path.join(path, item['keyword']))
                path = os.path.join(path, item['keyword'])

            with open(os.path.join(path, '%s.jpg' % str(item['id'])), 'wb') as f:
                f.write(item['data'])
        # return item
