import time
import scrapy
from scrapy import *
from tqdm import tqdm
from ..settings import *
from ..items import DataItem
from ..filter import ArtworkFilter
from ..filters.ImageFilter import ImageFilter
from ..filters.TagsFilter import TagsFilter

ARTWORK_FILETER = ArtworkFilter()
ARTWORK_FILETER.add_filter(TagsFilter())
ARTWORK_FILETER.add_filter(ImageFilter())

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
        data['tags'] = response.meta['info']['tags']
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
