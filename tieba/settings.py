# -*- coding: utf-8 -*-

# Scrapy settings for tieba project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tieba'

SPIDER_MODULES = ['tieba.spiders']
NEWSPIDER_MODULE = 'tieba.spiders'

ITEM_PIPELINES = {
    'tieba.pipelines.JSONPipeline1': 100,
    'tieba.pipelines.JSONPipeline2': 200
}
# LOG_LEVEL = 'INFO'
# LOG_FILE = 'log'
USER_AGENT = 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'

COOKIES_ENABLED = False

CONCURRENT_REQUESTS = 100