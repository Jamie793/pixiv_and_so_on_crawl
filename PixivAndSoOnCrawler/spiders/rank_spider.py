import time
import scrapy
from scrapy import *
from tqdm import tqdm
from ..settings import *
from .spider_utils import *

class RankSpider(scrapy.Spider):
    name = 'rank'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.cur_page = 1

        self.page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        if self.r18:
            RANK_TYPE + '_r18'

        self.tqdm = tqdm(total=0)

    def start_requests(self):
        print('\nStarting...')
        print(
            f'Spider: pixiv_rank_spider\nTotal page: {self.page}\nR-18 mode: {self.r18}\nRank date: {RANK_DATE}')
        yield Request(PIXIV_API['rank'].format(RANK_TYPE, RANK_DATE, self.cur_page), callback=self.parse)

    def parse(self, response, **kwargs):
        contents = response.json()['contents']
        if 'error' in contents or self.cur_page > self.page:
            return

        for i in contents:
            if ARTWORK_FILETER.filter(i):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': '%s_%s' % (RANK_TYPE, RANK_DATE)
                }, callback=self.parse_thumb)

        self.cur_page += 1
        yield Request(PIXIV_API['rank'].format(RANK_TYPE, RANK_DATE, self.cur_page), callback=self.parse)

    def parse_thumb(self, response):
        if ARTWORK_FILETER.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['illust_id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)
