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
    id = scrapy.Field()
    title = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    date = scrapy.Field()
    data = scrapy.Field()
    subtitle = scrapy.Field()
    ext = scrapy.Field()
    progress = scrapy.Field()
    tags = scrapy.Field()
    pass
