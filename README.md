# PixivAndSoOn Spider
## Introduce:green_book:
![](https://img.shields.io/badge/environment-python-green)
![](https://img.shields.io/badge/package-scrapy-blue)

This is spider based on scrapy . The spider can crawl "pixiv" artwork and so on. There are many options selected for you, you can set it by your hobby. The project provides many spider options.  
- If you just crawl by keyword, you can use "pixiv_keyword_spider".  
- If you just crawl by the rank board, you can use "pixiv_rank_spider".  
- If you just crawl by user, you can use "pixiv_user_rank_spider". 

## Install:blue_book:
This project uses python and scrapy. Go check them out if you don't have them locally installed. 

`pip -r requirements.txt`

## Usage:notebook:
This use spider prompt start it. For example.

`scrapy crawl pixiv_keyword_spider -a keyword=a -a page=10 -a r18=false`

The following options for you 

1. pixiv_keyword_spider
2. pixiv_rank_spider
3. pixiv_user_spider

## Configuration:orange_book:
You can config your spider in "settings.py"

- General
  - `Cookie`: User cookie, via type "javascript:prompt('cookie', document.cookie)" in navigation get it
  - `IMAGE_PAGE_NUM`: The image page num, per page 60 or 50 num
  - `REQUEST_PROXY`: The requests server proxy
  - `SAVE_DIR`: Image save directory
  - `ONE_KEYWORD_ONE_DIR`: If set true will make a directory of every keyword

- Keyword spider
  - `KEYWORD`: When keyword crawling is used, this keyword is used by default if it is not set

- Rank spider
  - `RANK_TYPE`: The type of crawl to be made
  - `RANK_DATE`: If not none, it will crawl before the RANK_DATE

- User spider
  - `USER_ID`: When using user spider, will use this user-id

- Filter
  - TAGS_FILTER
  - IMAGE_SIZE_FILTER
