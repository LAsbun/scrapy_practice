# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import Request
from os import rename

class OschinaPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)


    def item_completed(self, results, item, info):
        # print results
        baseurl = '/home/sws/scrapy_/image/'
        for ok, x in results:
            if ok:
                image_paths = x['path']
                real_name = x['url'].split('/')[-1]
                rename(baseurl+image_paths, baseurl+image_paths.split('/')[0]+real_name+'.jpg')

        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s'%image_paths)



    # def __init__(self):
    #     self.file = open("result.jl", 'w')
    #     self.seen = set() #重复检测集合
    #
    # def process_item(self, item, spider):
    #     if item['Link'] in self.seen:
    #         raise DropItem('Duplicate link %s ' %item['Link'])
    #
    #     self.seen.add(item['Link'])
    #
    #     line = json.dumps(dict(item), ensure_ascii=False)+'\n'
    #
    #     self.file.write(line)
    #     return item


# mongodb---stackoverflow

import pymongo

from scrapy.conf import settings
from scrapy import log

class MongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_POST']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise  DropItem('Missing {0}!'.format(data))

        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to Mongodb database!",
                    level=log.DEBUG, spider=spider)

        return item

class LagouPipeline(object):

    def __init__(self):
        con = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_POST']
        )
        db = con['lagou_test']

        db.lagou.create_index(
            [('positionId', pymongo.ASCENDING)],
            unique = True
        )
        self.collection = db['lagou']

    def process_item(self, item, spider):

        valid = True

        if item['positionId'] is None:
            valid = False
            raise DropItem('抓取失败')

        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to Mongodb database!",
                    level=log.DEBUG, spider=spider)

        yield item
