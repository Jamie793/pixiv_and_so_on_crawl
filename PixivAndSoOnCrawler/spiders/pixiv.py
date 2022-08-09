import time
import scrapy
from scrapy import *
from tqdm import tqdm

from ..filters.ImageFilter import ImageFilter
from ..filters.TagsFilter import TagsFilter
from ..items import DataItem
from ..settings import *
from ..filter import ArtworkFilter

artworkFilter = ArtworkFilter()
artworkFilter.add_filter(TagsFilter())
artworkFilter.add_filter(ImageFilter())


class SpiderUtils:

    @staticmethod
    def parse_image(self, response):
        data = []
        body = response.json()['body']
        if len(body) == 0:
            return

        for i, v in enumerate(body):
            self.tqdm.total += 1
            url: str = v['urls']['original']
            response.meta.update({
                'subtitle': '_p%d' % i,
                'ext': url.split('.')[-1]
            })
            data.append(Request(url, meta=response.meta,
                        callback=self.download_image))
        return data

    @staticmethod
    def download_image(self, response):
        data = DataItem()
        data['keyword'] = response.meta['keyword']

        if 'id' in response.meta['info']:
            data['id'] = response.meta['info']['id']
        elif 'illust_id' in response.meta['info']:
            data['id'] = response.meta['info']['illust_id']

        data['title'] = response.meta['info']['title']

        if 'userName' in response.meta['info']:
            data['user_name'] = response.meta['info']['userName']
        elif 'user_name' in response.meta['info']:
            data['user_name'] = response.meta['info']['user_name']

        if 'userId' in response.meta['info']:
            data['user_id'] = response.meta['info']['userId']
        elif 'user_name' in response.meta['info']:
            data['user_id'] = response.meta['info']['user_id']

        if 'createDate' in response.meta['info']:
            data['date'] = response.meta['info']['createDate']
        elif 'date' in response.meta['info']:
            data['date'] = response.meta['info']['date']

        data['data'] = response.body
        data['subtitle'] = response.meta['subtitle']
        data['ext'] = response.meta['ext']
        data['progress'] = self.tqdm
        return data


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

        self.tqdm = tqdm(total=0)

        if self.r18:
            PIXIV_API['search'] += '&mode=r18'

    def start_requests(self):
        print('\nStarting...')
        print(
            f'Spider: pixiv_keyword_spider\nKeyword: {self.keyword0}\nTotal page: {self.page}\nR-18 mode: {self.r18}')
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse(self, response):
        data = response.json()
        if len(data) == 0 or data['error'] or self.cur_page > self.page:
            return

        data = data['body']['illust']['data']

        for i in data:
            if artworkFilter.filter(i):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': response.meta['keyword'],
                }, callback=self.parse_thumb)

        self.cur_page += 1
        url = PIXIV_API['search'].format(
            self.keyword, self.keyword, self.cur_page)
        yield Request(url, meta={'keyword': self.keyword}, callback=self.parse)

    def parse_thumb(self, response):
        if artworkFilter.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)


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
            if artworkFilter.filter(i):
                yield Request(i['url'], meta={
                    'info': i,
                    'keyword': '%s_%s' % (RANK_TYPE, RANK_DATE)
                }, callback=self.parse_thumb)

        self.cur_page += 1
        yield Request(PIXIV_API['rank'].format(RANK_TYPE, RANK_DATE, self.cur_page), callback=self.parse)

    def parse_thumb(self, response):
        if artworkFilter.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['illust_id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)


class UserSpider(scrapy.Spider):
    name = 'pixiv_user_spider'

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
        if artworkFilter.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        return SpiderUtils.download_image(self, response)


class DiscoverySpider(scrapy.Spider):
    name = 'pixiv_discovery_spider'

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
            if artworkFilter.filter(i):
                yield Request(i['url'], meta={'info': i}, callback=self.parse_thumb)

        self.cur_page += 1
        if self.cur_page < self.page:
            yield Request(PIXIV_API['recommend'], callback=self.parse, dont_filter=True)

    def parse_thumb(self, response):
        if artworkFilter.filter(None, response):
            yield Request(PIXIV_API['artworks'].format(response.meta['info']['id']),
                          meta=response.meta, callback=self.parse_image)

    def parse_image(self, response):
        for i in SpiderUtils.parse_image(self, response):
            yield i

    def download_image(self, response):
        response.meta['keyword'] = "discovery_%s" % self.time
        return SpiderUtils.download_image(self, response)
