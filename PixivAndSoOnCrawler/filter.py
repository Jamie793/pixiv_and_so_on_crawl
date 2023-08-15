from PixivAndSoOnCrawler.settings import *

class ArtworkFilter:
    def __init__(self) -> None:
        self.filter_list = []

    def add_filter(self, filter):
        self.filter_list.append(filter)

    def filter(self, info, raw=None):
        flag = True
        for i in self.filter_list:
            flag &= i.filter(info, raw)

        return flag
