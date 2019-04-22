# -*- coding: utf-8 -*-

from scrapy import Field, Item

class PinduoduoGoodsItem(Item):
    table = 'goods'
    goods_id = Field()
    goods_name = Field()
    hd_url = Field()
    detail_url = Field()
    price = Field()
    sales = Field()
    tags = Field()
    mall_name = Field()