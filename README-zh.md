# PixivAndSoOn Spider
## Introduce:green_book:
![](https://img.shields.io/badge/environment-python-green)
![](https://img.shields.io/badge/package-scrapy-blue)

这是基于scrapy的蜘蛛。蜘蛛可以爬行“pixiv”艺术作品等等。有很多选项供你选择，你可以根据你的爱好设置。该项目提供了许多爬行器选项。
- 如果只是通过关键字抓取，可以使用 “pixiv_keyword_spider”。  
- 如果您只是浏览排名板，您可以使用 “pixiv_rank_spider”。  
- 如果只是按用户爬行，可以使用 “pixiv_user_rank_spider”。 

## Install:blue_book:
这个项目使用python和scrapy。如果你没有在本地安装，可以去看看。

`pip -r requirements.txt`

## Usage:notebook:
这个使用爬行器命令启动它。

`scrapy crawl ekyword -a keyword=a -a page=10 -a r18=false`

以下爬虫方案任你选择

1. user
2. rank
3. keyword
4. discovery

## Configuration:orange_book:
您可以在“settings.py”中配置爬行器。

- General
  - `Cookie`: 用户cookie，通过在导航中输入"javascript:prompt('cookie'， document.cookie)"获得它
  - `IMAGE_PAGE_NUM`: 插画页面数目，每页60或50个
  - `REQUEST_PROXY`: 请求服务器代理
  - `SAVE_DIR`: 插画保存目录
  - `ONE_KEYWORD_ONE_DIR`: 如果设置为True那么将会给每个关键字创建一个目录

- Keyword spider
  - `KEYWORD`: 使用关键字爬行时，如果未设置该关键字，则默认使用该关键字

- Rank spider
  - `RANK_TYPE`: 爬行器类型
  - `RANK_DATE`: 如果不为空将爬取之前的排行版

- User spider
  - `USER_ID`: 默认用户ID

- Filter
  - 自带了默认的过滤器
    - 标签过滤器
    - 插画大小过滤器
  - 你也可以通过修改spider_utils.py实现你自己的过滤器

