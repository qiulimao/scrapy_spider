#!/usr/bin/env python
#-*-coding:utf-8-*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Text,DateTime,Date 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Seebug(Base):
    """
        定义数据库映射
    """
    
    __tablename__ = "vul_seebug"
    
    id = Column(Integer,primary_key=True)
    title = Column(String(256),nullable=False)
    ssvid = Column(String(32),nullable=False)
    discover_time = Column(Date,nullable=True)
    commit_time = Column(Date,nullable=True)
    #PubTime  = Column(Date,nullable=True)
    danger_level = Column(String(8),nullable=False)
    bug_type = Column(String(32),nullable=True)
    cveid = Column(String(16),nullable=True)
    cnnydid = Column(String(16),nullable=True)
    cnvdid = Column(String(16),nullable=True)
    author = Column(String(16),nullable=True)
    commitor = Column(String(16),nullable=True)
    
    zoomeye_dork = Column(String(16),nullable=True)
    influence_component = Column(String(16),nullable=True)
    
    bug_abstract = Column(String(512),nullable=True)
    
    url = Column(String(256),nullable=False)
    
    url_md5 = Column(String(32),nullable=False,unique=True,default=func.md5(url))
    save_time = Column(DateTime,default=func.now())
    last_modified = Column(DateTime, onupdate=func.utc_timestamp())
    
    
class Wooyun(Base):
    """ 
        this is wooyun item model ;I used the raw python sql long ago,
    and said it must be a nightmare when it came to maintenance.
    it true,I have to rewirite the pipeline part with sqlalchemy now.
    NEVERL WILL I USE THE RAW WILL UNLESS NO APPROPRIOATE OPENSOURCE PROJECT !!
    qiulimao@2016.04
    
    """
    __tablename__ = "vul_wooyun"

    id = Column(Integer,primary_key=True)
    hole_series_num = Column(String(128),unique=True)
    title = Column(String(128),nullable=False)
    related_company = Column(String(128),nullable=True)
    author = Column(String(128),nullable=True)
    PubTime = Column(DateTime)
    public_time=Column(DateTime)
    hole_type = Column(String(128),nullable=True)
    damage_level = Column(String(128),nullable=True)
    hole_status = Column(String(128),nullable=True)
    hole_origin = Column(String(128),nullable=True)
    tags = Column(String(128),nullable=True)
    disclose_status = Column(String(512),nullable=True)
    hole_hash = Column(String(128),nullable=True)
    description = Column(String(512),nullable=True)
    hole_detail = Column(Text)
    hole_poc = Column(Text)
    hole_patch = Column(Text)
    company_reply = Column(Text)
    hole_detail_text = Column(Text)
    hole_poc_text = Column(Text)
    hole_patch_text = Column(Text)
    company_reply_text = Column(Text)
    saved_time = Column(DateTime,default=func.now())

if __name__ == "__main__":
    """
        直接用python运行这个文件则创建数据库表
        如果更改字段需要删除数据库中对应表格，并重新创建
    """
    Base.metadata.create_all(engine)
