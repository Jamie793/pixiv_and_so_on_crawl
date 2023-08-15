from PixivAndSoOnCrawler.filters.AbsArtworkFilter import AbsArtworkFilter
from PixivAndSoOnCrawler.settings import *

class ImageFilter(AbsArtworkFilter):
    def __init__(self) -> None:
        pass

    def filter(self, info, response=None):
        flag = True
        if info != None:
            if IMAGE_SIZE_FILTER:
                if IMAGE_MAXIMUM_WIDTH != 0 and info['width'] > IMAGE_MAXIMUM_WIDTH:
                    flag = False
                if IMAGE_MAXIMUM_HEIGHT != 0 and info['height'] > IMAGE_MAXIMUM_HEIGHT:
                    flag = False
                if IMAGE_MINIMUM_WIDTH != 0 and info['width'] < IMAGE_MINIMUM_WIDTH:
                    flag = False
                if IMAGE_MINIMUM_HEIGHT != 0 and info['height'] < IMAGE_MINIMUM_HEIGHT:
                    flag = False
        return flag
    