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
    
    __tablename__ = "seebug"
    
    id = Column(Integer,primary_key=True)
    title = Column(String(256),nullable=False)
    ssvid = Column(String(32),nullable=False)
    discover_time = Column(Date,nullable=False)
    commit_time = Column(Date,nullable=True)
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
    
    


if __name__ == "__main__":
    """
        直接用python运行这个文件则创建数据库表
        如果更改字段需要删除数据库中对应表格，并重新创建
    """
    Base.metadata.create_all(engine)