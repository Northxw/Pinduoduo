# -*- coding: utf-8 -*-
import base64

class ProxyMiddleware(object):
    def __init__(self, proxy_server, proxy_user, proxy_pass):
        self.proxy_server = proxy_server
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.proxy_auth = "Basic " + base64.urlsafe_b64encode(
            bytes((self.proxy_user + ":" + self.proxy_pass), "ascii")).decode("utf8")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_server=crawler.settings.get('PROXY_SERVER'),
            proxy_user=crawler.settings.get('PROXY_USER'),
            proxy_pass=crawler.settings.get('PROXY_PASS')
        )

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxy_server
        request.headers["Proxy-Authorization"] = self.proxy_auth

    def process_response(self, request, response, spider):
        return response