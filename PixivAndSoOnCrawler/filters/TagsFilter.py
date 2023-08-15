from PixivAndSoOnCrawler.filters.AbsArtworkFilter import AbsArtworkFilter
from PixivAndSoOnCrawler.settings import *

class TagsFilter(AbsArtworkFilter):
    def __init__(self) -> None:
        pass

    def filter(self, info, response=None):
        flag = True
        if info != None:
            if TAGS_FILTER == 1:
                flag = False
                for i in info['tags']:
                    if i in TAGS_LIST:
                        flag = True

            elif TAGS_FILTER == 2:
                flag = True
                for i in info['tags']:
                    if i in TAGS_LIST:
                        flag = False
        return flag