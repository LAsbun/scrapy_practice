#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from scrapy import Spider
from scrapy.selector import Selector

from scrapy_practice.items import StackItem


class StackSpider(Spider):
    name = 'stack'

    allowed_domains = [
        'stackoverflow.com',
    ]

    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        sel = Selector(response)

        items = sel.xpath(r'//div[@class="summary"]/h3')

        for i in items:
            item = StackItem()
            item['title']= i.xpath("a[@class='question-hyperlink']/text()").extract()[0]
            item['url'] = i.xpath("a[@class='question-hyperlink']/@href").extract()[0]


            print 'url'+'-'*10+item['url']
            print 'title'+'-'*10+item['title']
            yield  item