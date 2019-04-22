# -*- coding: utf-8 -*-

import random

BOT_NAME = 'pinduoduo'

SPIDER_MODULES = ['pinduoduo.spiders']
NEWSPIDER_MODULE = 'pinduoduo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pinduoduo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

DOWNLOAD_DELAY = eval('%.1f'%random.random())

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pinduoduo.middlewares.PinduoduoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'pinduoduo.middlewares.ProxyMiddleware': 543,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pinduoduo.pipelines.ImagePipeline': 270,
    'pinduoduo.pipelines.TextPipeline': 280,
    'pinduoduo.pipelines.ExcelPipeline': 290,
    'pinduoduo.pipelines.MysqlTwistedPipeline': 300,
}

IMAGES_STORE = './images/'

GOODS_NAME_LIST = ['iPad']

MAX_PAGES = 30

STATIC_NUM = 100

DOWNLOAD_TIMEOUT = 10

# MYSQL_HOST = 'localhost'
MYSQL_HOST = '192.168.1.184'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'pdd'
MYSQL_PORT = 3306

# SMTP SETTINGS
SMTP_HOST = 'smtp.163.com'
SMTP_USER = 'northxw@163.com'
SMTP_AUTHCODE = '123456'
SMTP_PORT = '465'
SENDER = 'northxw@163.com'
SUBJECT = 'Crawler Status Report'
RECEIVE_LIST = ['northxw@qq.com', 'northxw@sina.com']