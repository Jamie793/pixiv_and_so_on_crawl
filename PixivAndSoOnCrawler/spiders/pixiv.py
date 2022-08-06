
import time
import scrapy
from scrapy import *
from ..items import DataItem
from ..settings import *
from ..filter import ArtworkFilter

class KeywordSpider(scrapy.Spider):
    name = 'pixiv_keyword_spider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.cur_page = 1

        self.keyword = getattr(self, 'keyword', False) if getattr(
            self, 'keyword', False) else KEYWORD

        self.page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        if self.r18:
            PIXIV_API['search'] += '&mode=r18'

    def start_requests(self):
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse(self, response):
        data = response.json()
        if len(data) == 0 or data['error'] or self.cur_page > self.page:
            return

        data = data['body']['illust']['data']

        for i in data:
            if ArtworkFilter.filter_by_option(i, 'cz'):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': response.meta['keyword'],
                }, callback=self.parse_thumb)

        self.cur_page += 1
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse_thumb(self, response):
        if ArtworkFilter.filter_thumb(response.meta['info'], response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']), meta={
                'info': response.meta['info'],
                'keyword': response.meta['keyword']
            }, callback=self.parse_image)

    def parse_image(self, response):
        body = response.json()['body']
        if len(body) == 0:
            return
        for i in body:
            yield Request(i['urls']['original'], meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']
        data['id'] = response.meta['info']['id']
        data['title'] = response.meta['info']['title']
        data['user_name'] = response.meta['info']['userName']
        data['user_id'] = response.meta['info']['userId']
        data['date'] = response.meta['info']['createDate']
        data['data'] = response.body
        return data





class RankSpider(scrapy.Spider):
    name = 'pixiv_rank_spider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.cur_page = 1

        self.page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE

        if self.r18:
            RANK_TYPE + '_r18'

    def start_requests(self):
        yield Request(PIXIV_API['rank'].format(RANK_TYPE, RANK_DATE, self.cur_page), callback=self.parse)

    def parse(self, response, **kwargs):
        contents = response.json()['contents']
        if 'error' in contents or self.cur_page > self.page:
            return

        for i in contents:
            if ArtworkFilter.filter_by_option(i, option='zc'):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': '%s_%s' % (RANK_TYPE, RANK_DATE)
                }, callback=self.parse_thumb)

        self.cur_page += 1
        yield Request(PIXIV_API['rank'].format(RANK_TYPE, RANK_DATE, self.page), callback=self.parse)

    def parse_thumb(self, response):
        if ArtworkFilter.filter_thumb(response.meta['info'], response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['illust_id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        body = response.json()['body']
        if len(body) == 0:
            return
        for i in body:
            yield Request(i['urls']['original'], meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']
        data['id'] = response.meta['info']['illust_id']
        data['title'] = response.meta['info']['title']
        data['user_name'] = response.meta['info']['user_name']
        data['user_id'] = response.meta['info']['user_id']
        data['date'] = response.meta['info']['date']
        data['data'] = response.body
        return data






class UserSpider(scrapy.Spider):
    name = 'pixiv_user_spider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.user_id = str(int(getattr(self, 'id', False)) if getattr(
            self, 'id', False) else USER_ID)

    def start_requests(self):
        yield Request(PIXIV_API['user_profile'].format(self.user_id), meta={'user_id': self.user_id}, callback=self.parse)

    def parse(self, response, **kwargs):
        illusts = list(dict(response.json()['body']['illusts']).keys())
        lists = []
        for i in range(0, len(illusts), 10):
            s = i
            if i >= len(illusts) - 1:
                e = len(illusts)
            else:
                e = s + 10

            lists.append(illusts[s:e])

        for i in lists:
            data = ''
            for j in i:
                data += '&ids[]=' + str(j)
            yield Request(PIXIV_API['user_artwork'].format(self.user_id, data[1:]), meta=response.meta, callback=self.parse_info)

    def parse_info(self, response):
        data = dict(response.json()['body']['works'])
        for i in data.keys():
            k = data[i]
            if ArtworkFilter.filter_by_option(k, 'cz'):
                yield Request(k['url'], meta={'info': k, 'keyword': response.meta['user_id']}, callback=self.parse_thumb)

    def parse_thumb(self, response):
        if ArtworkFilter.filter_thumb(response.meta['info'], response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        body = response.json()['body']
        if len(body) == 0:
            return
        for i in body:
            yield Request(i['urls']['original'], meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']
        data['id'] = response.meta['info']['id']
        data['title'] = response.meta['info']['title']
        data['user_name'] = response.meta['info']['userName']
        data['user_id'] = response.meta['info']['userId']
        data['date'] = response.meta['info']['createDate']
        data['data'] = response.body
        return data















class DiscoverySpider(scrapy.Spider):
    name = 'pixiv_discovery_spider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.cur_page = 1

        self.page = int(getattr(self, 'page', False)) if getattr(
            self, 'page', False) else IMAGE_PAGE_NUM

        self.r18 = bool(getattr(self, 'r18', False)) if getattr(
            self, 'r18', False) else R18_MODE
        
        self.time = time.strftime('%Y-%m-%d_%H-%M-%S')

        type = 'all'
        if self.r18:
            type = 'r18'

        PIXIV_API['recommend'] = PIXIV_API['recommend'].format(type)


    def start_requests(self):
        for i in range(self.page + 1):
            yield Request(PIXIV_API['recommend'], callback=self.parse)

    def parse(self, response, **kwargs):
        illusts = response.json()['body']['thumbnails']['illust']
        for i in illusts:
            if ArtworkFilter.filter_by_option(i, 'zc'):
                yield Request(i['url'], meta={'info':i}, callback=self.parse_thumb)
        

    def parse_thumb(self, response):
        if ArtworkFilter.filter_thumb(response.meta['info'], response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        body = response.json()['body']
        if len(body) == 0:
            return
        for i in body:
            yield Request(i['urls']['original'], meta=response.meta, callback=self.download_image)

    def download_image(self, response):
        data = DataItem()
        data['keyword'] = 'discovery_%s' % self.time
        data['id'] = response.meta['info']['id']
        data['title'] = response.meta['info']['title']
        data['user_name'] = response.meta['info']['userName']
        data['user_id'] = response.meta['info']['userId']
        data['date'] = response.meta['info']['createDate']
        data['data'] = response.body
        return data
