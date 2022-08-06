from PixivAndSoOnCrawler.settings import *


class ArtworkFilter:

    @staticmethod
    def filter_tags(info):
        flag = True
        if TAGS_FILTER:
            flag = False
            for i in info['tags']:
                if i in TAGS_LIST:
                    flag = True

        return flag

    @staticmethod
    def filter_thumb(info, raw):
        return True

    @staticmethod
    def filter_image_by_size(info):
        flag = True

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

    @staticmethod
    def filter_by_option(info, option='', raw=None):
        # z: tags, x: thumb, c: size
        flag = True
        for i in option:
            if i == 'z':
                flag &= ArtworkFilter.filter_tags(info)
            elif i == 'x':
                flag &= ArtworkFilter.filter_thumb(info, raw)
            elif i == 'c':
                flag &= ArtworkFilter.filter_image_by_size(info)

        return flag
