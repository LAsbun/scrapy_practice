# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OschinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Link = scrapy.Field()
    LinkText = scrapy.Field()
    image_urls = scrapy.Field()



class MeniItem(scrapy.Item):

    image_urls = scrapy.Field()
    images = scrapy.Field()


# stackoverflow
# 提取问题以及url

class StackItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()

# 爬取拉勾网的某一求职顺序
class LagouItem(scrapy.Item):
    # ---- 主键相关

    # 主键 同时也是职位详细信息的页面的媒介
    positionId = scrapy.Field()

    # ----- 职位相关

    # 职位名称 python
    positionName = scrapy.Field()
    # 职位创建时间 2016-06-10
    createTime = scrapy.Field()
    # 职位类型
    positionType = scrapy.Field()
    # 工资/月薪 10k-20k (存储方式为一个列表 第一个是最低 第二个是最高)
    salary = scrapy.Field()
    # 全职/实习  全职
    jobNature = scrapy.Field()
    # 经验 3-5年
    workYear = scrapy.Field()
    # 职位所属方向 技术
    positionFirstType = scrapy.Field()
    # 学历要求 大专
    education = scrapy.Field()

    # 职位优势 技术氛围极好，领导超赞
    positionAdvantage = scrapy.Field()

    # 职位要求 以及 职位职责[2年以上Python开发经验]
    positionNeed = scrapy.Field()
    # # 职位职责 列表 [负责相关需求分析及系统设计；]  --因为暂时还没有找到相应的把要求和职责分开的方法，所以暂时存储在一起
    # positionDuty = scrapy.Field()

    # ----- 公司相关

    # 公司名 有云
    companyName = scrapy.Field()
    # 公司阶段  A轮
    financeStage = scrapy.Field()
    # 公司全称 有云有限公司
    companyShortName = scrapy.Field()
    # 公司福利 列表 ["绩效奖金" 岗位晋升 年度旅游, 扁平管理]
    companyLabelList = scrapy.Field()
    # 公司主营方向 "移动互联网 · 数据服务"
    industryField = scrapy.Field()
    # 工作地点 广州
    city = scrapy.Field()
    # 工作区 西湖区
    district = scrapy.Field()
    # 详细工作地址  数组 翠苑/文一路/高新文教区
    businessZones = scrapy.Field()

    # 其他不知道是什么的相关

    # pvScore 不知道具体是什么
    pvScore = scrapy.Field()
    # 分数 1356
    score = scrapy.Field()
    # realScore  好像都是1000
    relScore = scrapy.Field()
