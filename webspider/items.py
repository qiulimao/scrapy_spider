# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeeBugItem(scrapy.Item):
    """ this class is for www.seebug.org items """

    title = scrapy.Field()
    ssvid = scrapy.Field()
    discover_time = scrapy.Field()
    commit_time = scrapy.Field()
    danger_level = scrapy.Field()
    bug_type = scrapy.Field()
    
    cveid = scrapy.Field()
    
    cnnydid = scrapy.Field()
    cnvdid = scrapy.Field()
    
    author = scrapy.Field()
    commitor = scrapy.Field()
    
    zoomeye_dork = scrapy.Field()
    influence_component = scrapy.Field()
    
    bug_abstract = scrapy.Field()
    
    url = scrapy.Field()

class WooyunItem(scrapy.Item):
    """ this class is used for www.wooyun.org items """
    
    hole_series_num = scrapy.Field() #漏洞序列号，用作主键
    title = scrapy.Field()#漏洞标题
    related_company = scrapy.Field()#相关厂商
    author = scrapy.Field()#漏洞提交作者
    #commit_time = scrapy.Field()#提交时间
    PubTime = scrapy.Field()# 提交时间
    public_time = scrapy.Field()#公开时间
    
    hole_type = scrapy.Field()#漏洞类型
    damage_level = scrapy.Field()#危害等级
    hole_status = scrapy.Field()#漏洞状态
    hole_origin = scrapy.Field()#漏洞来源
    tags = scrapy.Field()#漏洞标签
    hole_hash = scrapy.Field()#漏洞hash
    disclose_status = scrapy.Field()#漏洞披露状态
    description = scrapy.Field()#漏洞描述
    hole_detail = scrapy.Field()#漏洞详情
    hole_poc = scrapy.Field()#漏洞证明
    hole_patch = scrapy.Field()#漏洞补丁
    company_reply = scrapy.Field()#厂商回应
    hole_detail_text = scrapy.Field()#漏洞详情
    hole_poc_text = scrapy.Field()#漏洞证明
    hole_patch_text = scrapy.Field()#漏洞补丁
    company_reply_text = scrapy.Field()#厂商回应

    saved_time = scrapy.Field()