#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import scrapy

from scrapy_practice.items import MeniItem

class ScrapyMeni(scrapy.Spider):
    """
    抓取 'http://www.metinfo.cn/demo/res001/342/' 的所有的图片
    """


    name = 'meni'

    allowed_domains = [
        'www.metinfo.cn',
    ]

    start_urls = [
        'http://www.metinfo.cn/demo/res001/342/',
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)

        image_urls = sel.css('img::attr(src)').extract()

        print image_urls
        print '*'*50

        url_links = sel.xpath('//a[@href]')

        for url_link in url_links:
            # print url_link
            url_link = str(url_link.re(r'href="(.*?)"')[0])
            if url_link and url_link != "javascript:;":
                if url_link.startswith(r'../'):
                    continue
                if not url_link.startswith('http'):
                    url_link = response.url+url_link
                print url_link
                yield scrapy.Request(url_link, callback=self.parse)












