# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SeebugPipeline(object):
    def process_item(self, item, spider):
    
        self.see_item(item)
        
        return item
    
    def see_item(self,item):
        for k,v in item.items():
            print "%s :%s" %(k,v)
            