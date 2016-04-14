# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .models import Seebug,Wooyun
from .models import session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import logging
from hashlib import md5

logger  = logging.getLogger(__name__)

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
            logger.info("$$$$$$(%s)[%d] %s is updated"%(spider.name,seebug_item_id.id,item['url']))           
        except NoResultFound:
            seebug_item = Seebug(**item)
            session.add(seebug_item)
            session.commit()
            logger.info(">>>>>>(%s)[%d]:%s"%(spider.name,seebug_item.id,item["title"]))
        
        return item 
    
class WooyunPipeline(object):

    def process_item(self,item,spider):
        item_series_num = item['hole_series_num']
        try:
            wooyun_item = session.query(Wooyun.id).filter(Wooyun.hole_series_num==item_series_num).one()
            session.query(Wooyun).filter(id==wooyun_item.id).update(item)
            session.commit()
            logger.info("$$$$$$(%s)[%d] %s is updated"%(spider.name,wooyun_item.id,item['hole_origin']))
        except NoResultFound:
            wooyun_item = Wooyun(**item)
            session.add(wooyun_item)
            session.commit()
            logger.info(">>>>>>(%s)[%d]:%s is saved"%(spider.name,wooyun_item.id,item["title"]))

        return item 
