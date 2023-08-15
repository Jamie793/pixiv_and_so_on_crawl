import time
import scrapy
from scrapy import *
from tqdm import tqdm
from ..settings import *
from .spider_utils import *


class KeywordSpider(scrapy.Spider):
    name = 'keyword'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.cur_page = 1

        self.keyword = getattr(self, 'keyword', False) if getattr(
            self, 'keyword', False) else KEYWORD

        self.page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        self.tqdm = tqdm(total=0)

        if self.r18:
            PIXIV_API['search'] += '&mode=r18'

    def start_requests(self):
        print('\nStarting...')
        print(
            f'Spider: pixiv_keyword_spider\nKeyword: {self.keyword}\nTotal page: {self.page}\nR-18 mode: {self.r18}')
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse(self, response):
        data = response.json()
        if len(data) == 0 or data['error'] or self.cur_page > self.page:
            return

        data = data['body']['illust']['data']

        for i in data:
            if ARTWORK_FILETER.filter(i):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': response.meta['keyword'],
                }, callback=self.parse_thumb)

        self.cur_page += 1
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse_thumb(self, response):
        if ARTWORK_FILETER.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)
