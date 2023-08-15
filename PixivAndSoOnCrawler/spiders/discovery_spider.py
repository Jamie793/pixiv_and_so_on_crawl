import time
import scrapy
from scrapy import *
from tqdm import tqdm
from ..settings import *
from .spider_utils import *




class DiscoverySpider(scrapy.Spider):
    name = 'discovery'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.cur_page = 1

        self.page = int(getattr(self, 'page', 1)) if getattr(
            self, 'page', 0) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        self.time = time.strftime('%Y-%m-%d_%H-%M-%S')

        self.tqdm = tqdm(total=0)

        type = 'all'
        if self.r18:
            type = 'r18'

        PIXIV_API['recommend'] = PIXIV_API['recommend'].format(type)

    def start_requests(self):
        print('\nStarting...')
        print(
            f'Spider: pixiv_discovery_spider\nTotal page: {self.page}\nR-18 mode: {self.r18}\nTime: {self.time}')
        yield Request(PIXIV_API['recommend'], callback=self.parse)

    def parse(self, response, **kwargs):
        illusts = response.json()['body']['thumbnails']['illust']
        for i in illusts:
            if ARTWORK_FILETER.filter(i):
                yield Request(i['url'], meta={'info': i}, callback=self.parse_thumb)

        self.cur_page += 1
        if self.cur_page < self.page:
            yield Request(PIXIV_API['recommend'], callback=self.parse, dont_filter=True)

    def parse_thumb(self, response):
        if ARTWORK_FILETER.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        response.meta['keyword'] = "discovery_%s" % self.time
        return SpiderUtils.download_image(self, response)
