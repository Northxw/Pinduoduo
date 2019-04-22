## 拼多多商品信息爬虫
&emsp; 通过拼多多商品API获取商品信息。

## 项目目录
&emsp; [待补充]

## 环境依赖
第三方库 | 描述
:---:|:---:
scrapy | pip3 install scrapy
execjs | pip3 install execjs
xlrd | pip3 install xlrd
pyecharts | pip3 install pyecharts
wordcloud | pip3 install wordcloud
jieba | pip3 install jieba
&emsp; 注意：上述安装均在Windows环境下进行时，可能会出现依赖不足而导致安装错误的情况，请自行谷歌解决。

## 解释说明
&emsp; 首先，拼多多商品信息接口很容易在谷歌浏览器中找到，但是接口请求中有三个未知参数。其中 filp 和 list_id 参数在网页源码中携带，正则匹配获取即可。而 anti_content 加密参数在每次请求时都需要携带，具体解密过程我不叙述（怕侵权），谷歌有很多。

&emsp; 其次，本项目的可视化部分略带针对性，如果需要匹配到其他商品，需要自行修改代码。

&emsp; 最后，不要设置随机UA中间件（亲测坑），拼多多对请求的请求头检查比较严格，可自行在网页中粘贴 User-Agent 即可。
```Python
......

headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    
......

yield Request(url=self.search_url + urlencode(data),
                          headers=self.headers,
                          callback=self.parse_goods_info,
                          errback=self.error_back,
                          dont_filter=True)
```
&emsp; 已实现的中间件：ProxyMiddleWare(未启用，暂时未发现IP反爬)，已实现的管道：ImagePipeline、TextPipeline、ExcelPipeline、MysqlTwisted。

## 数据分析
&emsp; （本次商品的数据分析仅针对搜索参数iPad）

![price_zone]()

![tags]()

![wordcloud]()

## 更新记录
- 2019/4/21 项目整体架构已完成，可正常获取数据。
- ...

## 项目部署
&emsp; [待补充]

## 运行
&emsp; 命令行：
```Python
>>> scrapy crawl pdd
```
&emsp; 命令行切换至项目中main.py所在目录下，运行命令：
```Python
>>> python main.py
```
&emsp; 或者 scrapyd-client 打包部署到本地服务器，然后运行命令：
```Python
>>> curl http://localhost:6800/schedule.json -d project=pinduoduo -d spider=pdd
```
&emsp; Gerapy 管理，依次执行如下命令：
```Python
>>> gerapy init
>>> gerapy migrate
>>> gerapy runserver
```
&emsp; Gerapy默认在8000端口开启 Gerapy 服务并提供了更加方便的爬虫控制（具体使用方法请自行谷歌）。

## 公告
&emsp; (技术无罪) 本代码仅作学习交流，若涉及拼多多侵权，请邮箱联系，将在第一时间处理。