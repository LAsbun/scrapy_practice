# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

import scrapy
# from scrapy import Selector]
# from scrapy import FormRequest
# import time

from scrapy_practice.items import LagouItem
from scrapy_practice.exceptions import DupliteException

class ScrapyLagouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["www.lagou.com",]
    start_urls = [
        'http://www.lagou.com/jobs/list_php',
    ]

    def start_requests(self):
        return [
            scrapy.FormRequest(url="http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false",
                               method='post',
                               callback=self.total_pages,
                               formdata={
                                   'first':'false',
                                   'kd':'python',
                                   'pn':'1'
                               }
                               )
        ]

    def __init__(self):
        super(ScrapyLagouSpider, self).__init__()
        self.url_set = set()


    # 抓取一共有多少条数据，然后依次分页抓取
    def total_pages(self, response):
        # print 'sa'
        result = json.loads(response.body,encoding='utf-8')
        # print result['content']['positionResult']['totalCount']
        total_count = result['content']['positionResult']['totalCount']
        total_page =  total_count/15

        self.parse1(response)

        for i in range(3,4):
            yield scrapy.FormRequest(
                url="http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false",
                method='post',
                callback=self.parse1,
                formdata={
                    'first':'false',
                    'kd':'python',
                    'pn':str(i)
                }
            )


    def parse3(self, res):

        item = LagouItem()

        # 主键 同时也是职位详细信息的页面的媒介
        item['positionId'] = res['positionId']

        # print item['positionId']

        # ----- 职位相关

        # 职位名称 python
        item['positionName'] = res['positionName']
        # 职位创建时间 2016-06-10
        item['createTime'] = res['createTime']
        # 职位类型
        item['positionType'] = res['positionType']
        # 工资/月薪 10k-20k (存储方式为一个列表 第一个是最低 第二个是最高)
        item['salary'] = res['salary']
        # 全职/实习  全职
        item['jobNature'] = res['jobNature']
        # 经验 3-5年
        item['workYear'] = res['workYear']
        # 职位所属方向 技术
        item['positionFirstType'] = res['positionFirstType']
        # 学历要求 大专
        item['education'] = res['education']

        # 职位优势 技术氛围极好，领导超赞
        item['positionAdvantage'] = res['positionAdvantage']

        # # 职位要求 [2年以上Python开发经验]
        # item['positionNeed'] = res['']
        # # 职位职责 列表 [负责相关需求分析及系统设计；]
        # item['positionDuty'] = res['']

        # ----- 公司相关

        # 公司名 有云
        item['companyName'] = res['companyName']
        # 公司阶段  A轮
        item['financeStage'] = res['financeStage']
        # 公司全称 有云有限公司
        item['companyShortName'] = res['companyShortName']
        # 公司福利 列表 ["绩效奖金" 岗位晋升 年度旅游, 扁平管理]
        item['companyLabelList'] = res['companyLabelList']
        # 公司主营方向 "移动互联网 · 数据服务"
        item['industryField'] = res['industryField']
        # 工作地点 广州
        item['city'] = res['city']
        # 工作区 西湖区
        item['district'] = res['district']
        # 详细工作地址  数组 翠苑/文一路/高新文教区
        item['businessZones'] = res['businessZones']

        # 其他不知道是什么的相关

        # pvScore 不知道具体是什么
        item['pvScore'] = res['pvScore']
        # 分数 1356
        item['score'] = res['score']
        # realScore  好像都是1000
        item['relScore'] = res['relScore']
        # item['test1'] = result['content']['positionResult']['result'][0]['positionId']

        request = scrapy.Request(
            "http://www.lagou.com/jobs/"+str(item['positionId'])+".html",
            callback=self.parse2
        )
        # print request.body
        request.meta['item'] = item
        # print 'sssss'
        return request

    # parse1是抓取positionId，并且Request对应的网页抓取网页中的要求

    def parse1(self, response):
        # print response.url
        result = json.loads(response.body, encoding='utf-8')

        for res in result['content']['positionResult']['result']:
            yield self.parse3(res)



    def parse2(self, response):
        print response.url
        # print 'dsadsadsadsads'
        bsobj = BeautifulSoup(response.body, 'lxml')
        ss = bsobj.find(name='dd', attrs={'class':'job_bt'})
        # print ss.get_text()

        # with open('t1.txt', 'a+') as f:
        #     f.writelines(ss.get_text())
        #     f.write("\n")
        item = response.meta['item']
        item['positionNeed'] = ss.get_text()

        print item['positionId']
        return item
