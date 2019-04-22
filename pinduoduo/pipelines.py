# -*- coding: utf-8 -*-

import logging
import pymysql
from twisted.enterprise import adbapi
from openpyxl import Workbook
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

# 统计下载图片总量
COUNT_DOANLOAD_IMAGE = {'IMAGE_NUMBER': 0}

class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok ]
        if not image_paths:
            raise DropItem("Image Download Failed")
        COUNT_DOANLOAD_IMAGE['IMAGE_NUMBER'] += 1
        return item

    def get_media_requests(self, item, info):
        if item['hd_url']:
            yield Request(item['hd_url'])

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls,crawler):
        params = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DB'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **params)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item, spider)
        query.addErrback(self.handle_error, spider)

    def handle_error(self, failure, spider):
        spider.crawler.stats.inc_value('Failed_Insert_DB')
        logging.error("Failed Insert DB: %s" % failure)

    def do_insert(self, cursor, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(
            table=item.table, keys=keys, values=values)
        update = ', '.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        cursor.execute(sql, tuple(data.values())*2)
        spider.crawler.stats.inc_value('Success_Inserted_DB')

class ExcelPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['goods_id', 'goods_name', 'hd_url', 'detail_url', 'price', 'sales', 'tags', 'mall_name'])

    def process_item(self, item, spider):
        data = dict(item)
        line_data = [''.join(str(value)) for value in data.values()]
        self.ws.append(line_data)
        self.wb.save('./utils/pdd.xlsx')
        spider.crawler.stats.inc_value('Success_Append_Excel')
        return item

class TextPipeline(object):
    def open_spider(self, spider):
        self.file = open('./utils/pdd.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        string = item['goods_name'] + ' ' + item['tags']
        self.file.write('{}\n'.format(string))
        spider.crawler.stats.inc_value('Success_Append_Text')
        return item

    def close_spider(self, spider):
        self.file.close()