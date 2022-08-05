# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    pass



class DataItem(scrapy.Item):
    # define the fields for your item here like:
    keyword = scrapy.Field()
    info = scrapy.Field()
    type = scrapy.Field()
    id = scrapy.Field()
    data = scrapy.Field()
    pass
