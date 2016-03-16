#!/usr/bin/env python
#-encoding:utf-8-
from __future__ import with_statement

import os
import sys
import ConfigParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings




if __name__ == "__main__":

    current_path = os.path.dirname(os.path.abspath(__file__))

    if current_path not in sys.path:
        sys.path.append(current_path)

    
    #find the scrapy.cfg file
    config_file = os.path.join(current_path,'scrapy.cfg')
    
    #get a configureParser
    config_parser=ConfigParser.ConfigParser()
    
    #the purpose of open scrapy.cfg is to set the environment path of SCRAPY_SETTINGS_MODULE
    with open(config_file,'r') as configures:
        config_parser.readfp(configures)
        settings_module= config_parser.get('settings','default')
        os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module
        timing_spiders = config_parser.options("timing_spiders")
     
    process = CrawlerProcess(get_project_settings())
    
    for spider in timing_spiders:
        process.crawl(spider)
    process.start()
