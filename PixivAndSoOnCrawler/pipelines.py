# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import re
from urllib.request import Request
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
            name = ARTWORK_Title.replace('{id}', str(item['id']))\
                .replace('{title}', re.sub('[\||/|:|\*|\?|"|<|>]', '', item['title'].replace('\\','')))\
                .replace('{user_name}', item['user_name'])\
                .replace('{user_id}', str(item['user_id']))\
                .replace('{date}', item['date'])\
                .replace('{tags}', ARTWORK_TAG_SPLIT.join(item['tags']))

            name += item['subtitle']

            with open(os.path.join(path, '%s.%s' % (name, item['ext'])), 'wb') as f:
                f.write(item['data'])
                item['progress'].update(item['progress'].pos +1)
                
        # return item
