import scrapy
from scrapy import *
from ..items import DataItem
from ..settings import *




class KeywordSpider(scrapy.Spider):
    name = 'pixiv_keyword_spider'
    keyword = 'xiao'

    def start_requests(self):
        keyword = getattr(self, 'keyword', False) if getattr(
            self, 'keyword', False) else keyword
        page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM
        r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        for i in range(1, page + 1):
            url = PIXIV_API['search'].format(keyword, keyword, i)
            if r18:
                url += '&mode=r18'

            yield Request(url, meta={'keyword': keyword}, callback=self.parse)

    def parse(self, response):
        data = response.json()['body']['illust']['data']
        for i in data:
            yield Request(i['url'], meta={
                'info': i,
                'keyword': response.meta['keyword'],
            }, callback=self.parse_thumb)

    def parse_thumb(self, response):
        if response:
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']), meta={
                'info': response.meta['info'],
                'keyword': response.meta['keyword']
            }, callback=self.parse_image)

    def parse_image(self, response):
        url = response.xpath(
            "//link[@rel='preload' and @as='image']/@href").get()
        yield Request(url, meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']
        data['id'] = response.meta['info']['id']
        data['data'] = response.body
        return data


class RankSpider(scrapy.Spider):
    name = 'pixiv_rank_spider'

    def start_requests(self):
        for i in range(1, RANK_PAGE_MAXIMUM + 1):
            type = ''
            if R18_MODE:
                type = '_r18'
            yield Request(PIXIV_API['rank'].format(RANK_TYPE + type, RANK_DATE, i), callback=self.parse)

    def parse(self, response, **kwargs):

        contents = response.json()['contents']

        for i in contents:
            yield Request(i['url'], meta={
                'info': i,
                'keyword': '%s_%s' % (RANK_TYPE, RANK_DATE)
            }, callback=self.parse_thumb)

    def parse_thumb(self, response):
        if response:
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['illust_id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        url = response.xpath(
            "//link[@rel='preload' and @as='image']/@href").get()
        yield Request(url, meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']
        data['id'] = response.meta['info']['illust_id']
        data['data'] = response.body
        return data
