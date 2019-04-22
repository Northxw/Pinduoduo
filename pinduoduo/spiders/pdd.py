# -*- coding: utf-8 -*-
import scrapy
import re
import json
import execjs
from urllib.request import quote
from urllib.parse import urlencode
from scrapy import Request
from pinduoduo.items import PinduoduoGoodsItem
from pinduoduo.pipelines import COUNT_DOANLOAD_IMAGE
import time
from pinduoduo.view import view, showcloud
from pinduoduo.email import EmailSender

class PddSpider(scrapy.Spider):
    # 爬虫启动时间
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'pdd'
    allowed_domains = ['yangkeduo.com/']
    # 商品信息API
    search_url = 'http://apiv3.yangkeduo.com/search?'
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }

    def start_requests(self):
        """
        请求搜索页
        """
        for goods in self.settings.get('GOODS_NAME_LIST'):
            url = 'http://yangkeduo.com/search_result.html?search_key=' + quote(goods)
            yield Request(url, callback=self.get_parameters, errback=self.error_back, meta={'goods_name': goods})

    def get_parameters(self, response):
        """
        获取参数：list_id, flip, anti_content
        """
        self.crawler.stats.inc_value("Success_Reqeust")
        goods_name = response.meta['goods_name']
        list_id = re.findall('"listID":"(.*?)"', response.text, re.S)[0]
        flip = re.findall('"flip":"(.*?)"', response.text, re.S)[0]
        with open('./utils/anti_content.js', 'r', encoding='utf-8') as f:
            js = f.read()
        for page in range(1, self.settings.get('MAX_PAGES') + 1):
            anti_content = execjs.compile(js).call('get_anti', response.url)
            data = {
                'gid': '',
                'source': 'search',
                'search_met': 'manual',
                'requery': '0',
                'list_id': list_id,
                'sort': 'default',
                'filter': '',
                'q': goods_name,
                'page': page,
                'size': '50',
                'flip': flip,
                'anti_content': anti_content,
                'pdduid': '0'
            }
            yield Request(url=self.search_url + urlencode(data),
                          headers=self.headers,
                          callback=self.parse_goods_info,
                          errback=self.error_back,
                          dont_filter=True)

    def parse_goods_info(self, response):
        """
        获取商品信息
        """
        if response:
            self.crawler.stats.inc_value("Success_Reqeust")
            items = json.loads(response.text)['items']
            for item in items:
                data = PinduoduoGoodsItem()
                data['goods_id'] = str(item['goods_id'])
                data['goods_name'] = item['goods_name']
                data['hd_url'] = item['hd_url']
                data['detail_url'] = 'http://yangkeduo.com/{}'.format(item['link_url'])
                data['price'] = int(item['price'] / (self.settings.get('STATIC_NUM')))
                data['sales'] = item['sales']
                data['tags'] = ' '.join([tag['text'] for tag in item['tag_list']])
                try:
                    data['mall_name'] = item['mall_name']
                except:
                    data['mall_name'] = ''
                self.logger.debug(data)
                yield data
        else:
            self.logger.debug("No data obtained!")

    def error_back(self, e):
        self.crawler.stats.inc_value("Failed_Request")
        self.logger.error('Something Error:{}'.format(e.args))

    def close(self, reason):
        """
        绘图、词云、发送邮件
        """
        # 可视化
        view()
        # 词云
        showcloud()
        # 发送邮件
        email = EmailSender()
        spider_name = self.settings.get('BOT_NAME')
        start_time = self.start
        success_request = self.crawler.stats.get_value("Success_Reqeust")
        failed_request = self.crawler.stats.get_value("Failed_Request")
        if failed_request == None:
            failed_request = 0
        insert_into_success = self.crawler.stats.get_value("Success_Inserted_DB")
        failed_db = self.crawler.stats.get_value("Failed_Insert_DB")
        if failed_db == None:
            failed_db = 0
        success_append_excel = self.crawler.stats.get_value('Success_Append_Excel')
        fnished_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        body = "爬虫名称：{}\n\n 开始时间：{}\n\n 请求成功总量：{}\n 请求失败总量：{}\n\n 数据库存储总量：{}\n 数据库存储失败总量：{}\n\n 图片下载总量：{}\nExcel存储成功总量：{}\n\n 结束时间  : {}\n".format(
            spider_name,
            start_time,
            success_request,
            failed_request,
            insert_into_success,
            failed_db,
            COUNT_DOANLOAD_IMAGE['IMAGE_NUMBER'],
            success_append_excel,
            fnished_time
        )
        try:
            email.sendEmail(self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)
        except:
            pass