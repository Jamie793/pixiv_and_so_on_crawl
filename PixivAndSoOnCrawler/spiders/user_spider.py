import time
import scrapy
from scrapy import *
from tqdm import tqdm
from ..settings import *
from .spider_utils import *


class UserSpider(scrapy.Spider):
    name = 'user'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.user_id = str(int(getattr(self, 'id', False)) if getattr(
            self, 'id', False) else USER_ID)

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        if self.r18:
            PIXIV_API['user_artwork'] += 'R-18'

        self.total = 0

        self.offset = 0

        self.tqdm = tqdm(total=0)

    def start_requests(self):
        print('\nStarting...')
        print(f'Spider: pixiv_user_spider\nUser-id: {self.user_id}\nR-18 mode: {self.r18}')
        yield Request(PIXIV_API['user_artwork'].format(self.user_id, self.offset), meta={'user_id': self.user_id}, callback=self.parse)

    def parse(self, response, **kwargs):
        body = response.json()['body']
        if self.total == 0:
            self.total = body['total']
            # print('Total: %d' % self.total )
        
        works = body['works']
        self.offset += len(works)
        for i in works:
            yield Request(i['url'],meta={'info':i, 'keyword':'user_%s' % str(self.user_id)}, callback=self.parse_thumb)
        
        if self.offset < self.total:
            yield Request(PIXIV_API['user_artwork'].format(self.user_id, self.offset), meta={'user_id': self.user_id}, callback=self.parse)


    def parse_thumb(self, response):
        if ARTWORK_FILETER.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)

