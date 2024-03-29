# Scrapy settings for PixivAndSoOnCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'PixivAndSoOnCrawler'

SPIDER_MODULES = ['PixivAndSoOnCrawler.spiders']
NEWSPIDER_MODULE = 'PixivAndSoOnCrawler.spiders'


# ======================================START===========================================

# User configuration
# The image page num, per page 60 or 50 num
IMAGE_PAGE_NUM = 50

# When keyword crawling is used, this keyword is used by default if it is not set
KEYWORD = ''

#When using user spider, will use this user-id
USER_ID = ''
# The need to crawl rank type
# type:
#   daily
#   weekly
#   monthly
#   rookie

RANK_TYPE = 'monthly'

# If not none, it will crawl before the RANK_DATE
# Warnings: A error value, will be 404 nof found
RANK_DATE = '20220801'

# Proxy
REQUEST_PROXY = 'http://localhost:20171'

# Image save path
SAVE_DIR = 'PixivAndSoOnCrawler/images'

# Title format template
#   {id}, {title}, {user_name}, {user_id}, {user_date}, {tags}
ARTWORK_Title = '{tags}'
ARTWORK_TAG_SPLIT = ' '

# If set true will make a directory of every keyword
ONE_KEYWORD_ONE_DIR = True

# If set, only crawl r18
R18_MODE = False

# 0: None 
# 1:only crawl in tags 
# 2:except tags
TAGS_FILTER = 2
TAGS_LIST = ''.join(['Genshin', "AI", "原神", "GenshinImpact"])


# If set as true, only crawl size of MINMUM to MAXMUM
IMAGE_SIZE_FILTER = True
IMAGE_MINIMUM_WIDTH = 0
IMAGE_MINIMUM_HEIGHT = 0

IMAGE_MAXIMUM_WIDTH = 0
IMAGE_MAXIMUM_HEIGHT = 0

# User Cookie
Cookie = ''

# DOWNLOAD_DELAY = 1 #(s)

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16



# =======================================END===========================================


PIXIV_API = {
    'search': 'https://www.pixiv.net/ajax/search/illustrations/{}?word={}&order=date_d&p={}&s_mode=s_tag&type=illust_and_ugoira&lang=zh',
    'artworks': 'https://www.pixiv.net/ajax/illust/{}/pages?lang=zh',
    'rank': 'https://www.pixiv.net/ranking.php?mode={}&content=illust&date={}&p={}&format=json',
    # 'user_profile':'https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh',
    'user_artwork':'https://www.pixiv.net/ajax/user/{}/illustmanga/tag?&offset={}&limit=48&lang=zh&tag=',
    'recommend':'https://www.pixiv.net/ajax/discovery/artworks?mode={}&limit=60&lang=zh'
}



# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

REDIRECT_ENABLED = False

# LOG_LEVEL = 'ERROR'

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Language': 'en',
    'referer': 'https://www.pixiv.net/',
    'authority': 'www.pixiv.net',
    'Cookie': Cookie,
}


# Obey robots.txt rules
# ROBOTSTXT_OBEY = False


# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs


# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False



# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'PixivAndSoOnCrawler.middlewares.PixivandsooncrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'PixivAndSoOnCrawler.middlewares.PixivandsooncrawlerDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'PixivAndSoOnCrawler.pipelines.PixivandsooncrawlerPipeline': 300,
}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
