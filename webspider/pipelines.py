# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import Seebug
from .models import session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import logging
from hashlib import md5

class SeebugPipeline(object):
    def process_item(self, item, spider):
        """
            采用sqlalchemy将数据存入数据库
            先根据url的md5查一下，有就跟新，没有就添加
        """
        item_url_md5 = md5(item["url"]).hexdigest()      
        try:
            seebug_item_id = session.query(Seebug.id).filter(Seebug.url_md5==item_url_md5).one()            
            session.query(Seebug).filter(id==seebug_item_id.id).update(item)
            session.commit()
            logging.info("[%d] %s is in the database$$$$$$"%(seebug_item_id.id,item['url']))           
        except NoResultFound:
            seebug_item = Seebug(**item)
            session.add(seebug_item)
            session.commit()
            logging.info(">>>>>>[%d]:%s"%(seebug_item.id,item["title"]))
        
        return item 
    
            