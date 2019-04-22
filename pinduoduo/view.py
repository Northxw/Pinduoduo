# -*- coding:utf-8 -*-

import xlrd
import os
import pyecharts
from wordcloud import WordCloud
import cv2
import jieba
import matplotlib.pyplot as plt

def view():
    """
    价格柱状图
    """
    # Excel存储路径
    excel_path = os.path.dirname(os.path.realpath(__file__)) + '\\utils\\pdd.xlsx'
    # 激活表格
    wb = xlrd.open_workbook(filename=excel_path)
    # sheet
    sheet_name = wb.sheet_names()[0]
    # sheet 内容
    sheet_content = wb.sheet_by_name(sheet_name)
    # 获取第五列所有价格
    cols_price = sheet_content.col_values(4)[1:]
    # 统计各价格区间的商品总量
    price_zone = {
        'less_than_1000': 0,        # 非正常价格
        'less_than_2000': 0,        # 1000-2000
        'less_than_3000': 0,        # 2000-3000
        'less_than_4000': 0,        # 3000-4000
        'greater_than_4000': 0,     # 大于4000
    }
    for price in cols_price:
        pirce_ = int(price)
        if  pirce_ > 4000:
            price_zone['greater_than_4000'] += 1
        elif pirce_ > 3000 and pirce_ <= 4000:
            price_zone['less_than_4000'] += 1
        elif pirce_ > 2000 and pirce_ <= 3000:
            price_zone['less_than_3000'] += 1
        elif pirce_ > 1000 and pirce_ <= 2000:
            price_zone['less_than_2000'] += 1
        else:
            price_zone['less_than_1000'] += 1

    data = []
    labels = []
    for k,v in price_zone.items():
        data.append(v)
        labels.append(k)

    bar = pyecharts.Bar("各价格区间的商品数量", 'https://github.com/Northxw/')
    bar.add('', labels, data, bar_category_gap="30%")
    bar.render(path=os.path.dirname(os.path.realpath(__file__)) + '\\view\\price.html')

    # 获取第六列标签数据
    cols_tags = sheet_content.col_values(6)[1:]
    tags = {
        '顺丰包邮': 0,
        '极速退款': 0,
        '退货包运费': 0,
        '品牌馆': 0,
        '全国联保': 0,
    }
    for tag in cols_tags:
        if '顺丰包邮' in tag:
            tags['顺丰包邮'] += 1
        elif '极速退款' in tag:
            tags['极速退款'] += 1
        elif '退货包运费' in tag:
            tags['退货包运费'] += 1
        elif '品牌馆' in tag:
            tags['品牌馆'] += 1
        elif '全国联保' in tag:
            tags['全国联保'] += 1

    data = []
    labels = []
    for k, v in tags.items():
        data.append(v)
        labels.append(k)

    pie = pyecharts.Pie("商家标签", 'https://github.com/Northxw/')
    pie.add('', labels, data, is_label_show=True)
    pie.render(path=os.path.dirname(os.path.realpath(__file__)) + '\\view\\tags.html')


def showcloud():
    # 文本路径
    text_path = os.path.dirname(os.path.realpath(__file__)) + '\\utils\\pdd.txt'
    if text_path:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        cut_text = " ".join(jieba.cut(text))
        color_mask = cv2.imread('./view/show.jpg')
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path="./view/FZSTK.TTF",
            # 设置背景色
            background_color='white',
            # 词云形状
            mask=color_mask,
            # 允许最大词汇
            max_words=2000,
            # 最大号字体
            max_font_size=40
        )
        wCloud = cloud.generate(cut_text)
        wCloud.to_file('./view/pdd.png')

        plt.imshow(wCloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    # view()
    showcloud()
