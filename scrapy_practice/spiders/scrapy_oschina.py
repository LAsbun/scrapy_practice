# -*- coding: utf-8 -*-
import scrapy

from scrapy_practice.items import OschinaItem
# 这个文件是通过 scrapy genspider scrapy_oschina scrapy_.net 来生成的
# scrapy genspider 爬虫名 要爬取的域名


class ScrapyOschinaSpider(scrapy.Spider):
    name = "oschina"
    # allowed_domains = ["scrapy_.net"]
    # start_urls = (
    #     'http://www.scrapy_.net/',
    # )

    allowed_domains = [
        'www.metinfo.cn',
    ]

    start_urls = [
        'http://www.metinfo.cn/demo/res001/342/',
    ]

    def parse(self, response):

        sel = scrapy.Selector(response)
        link_in_a_page = sel.xpath('//a[@href]')

        for link_sel in link_in_a_page:
            item = OschinaItem()
            link = str(link_sel.re('href="(.*?)"')[0]) # 每一个url
            if link:
                if link.startswith(r'../'):
                    continue
                    # link = '/'.join(link.split('/')[:-1])
                if not link.startswith('http'): #处理相对url
                    link = response.url+link

                # print link
                yield scrapy.Request(link, callback=self.parse) #生成新的请求，递归回调self.parse

                image_urls = sel.css('img::attr(src)').extract()

                real_image_urls = []
                for i in image_urls:
                    # i = str(i)
                    if i.startswith("../"):
                        i = i.replace('../', '')

                    real_image_urls.append('http://www.metinfo.cn/demo/res001/342/'+i)

                item['image_urls'] = real_image_urls

                item['Link'] = link
                link_text = link_sel.xpath('text()').extract()
                if link_text:
                    item['LinkText'] = str(link_text[0].encode('utf-8').strip())
                else:
                    item['LinkText'] = None
                # print item['Link']
                # print item['LinkText']
                yield  item
