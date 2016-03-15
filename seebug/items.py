# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BugItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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
