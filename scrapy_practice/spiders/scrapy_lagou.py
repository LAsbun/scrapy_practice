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



        # item['test2'] = response.xpath('//dd[@class="job_bt"]/h3/text()')[0].extract()

        # print response.css('dd[class="job_bt"]::text').extract()


        # for res in  result['content']['positionResult']['result']:
        #
        #     posid =  res['positionId']
        #     print posid
        #     if posid in self.url_set:
        #         raise DupliteException('又重复')
        #     else:
        #         self.url_set.add(posid)



        # for res in result['content']['positionResult']['result']:
        #     print '-'*10
        #     for k, v in res.items():
        #         if isinstance(v, list):
        #             print k, ': ',''.join([x for x in v])
        #             continue
        #         print k,': ', v
        # print type(res)
        # with open('tt.txt', 'w') as f:
        #     f.write(res)
        # sel = Selector(response)
        #
        # # a = sel.xpath('//div[@class="s_position_list"]/ul/li')
        # a = sel.xpath('//*[@id="s_position_list"]/ul/li[2]/div[1]/div[1]/div[1]/span')
        #
        #
        # print a
        # for k, v in  res['content']['positionResult']['result'][0].items():
        #     print k,' '*10, v
        # self.print_func(res, 0)
        # print res['content']['positionResult']['result'][0]

    def print_func(self, res, id):

        for i in res:
            if isinstance(res[i], dict):
                print i,' '*50, id
                self.print_func(res[i], id+1)
            else:
                print i,' '*50, id
                print res[i]


# with open('../../t.txt', 'rb') as f:
#     for i in f.readlines():
#         print json.loads(i, encoding='utf-8')
#
# for i in f.readlines():
#     print i
"""
测试

import requests

header = {
    'Cookie':'LGUID=20160521215119-186dde26-1f5b-11e6-9dd9-525400f775ce; tencentSig=2814602240; LGMOID=20160609104124-C714DB27859FAA308F26E218FD83B45C; HISTORY_POSITION=493225%2C8k-15k%2C%E5%A6%99%E8%AE%A1%E6%97%85%E8%A1%8C%2CPython%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88%7C; JSESSIONID=A26E899DA05D87E86B13FBCA773F79D1; login=true; unick=sws; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=19; _gat=1; SEARCH_ID=a60bd4bc419e4db9bd8bc3d4dc1306cc; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1463841765,1464833438,1465440085,1465449440; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1465459276; LGSID=20160609143734-a67e24a6-2e0c-11e6-a304-5254005c3644; LGRID=20160609160115-56e00e81-2e18-11e6-a305-5254005c3644; _ga=GA1.2.1835050123.1463838679',


}

data = {
    'first':'false',
    'kd':'Python',
    'pn':'2'
}

res = requests.post(url="http://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false", data=data)

print res.content

"""