#!/usr/bin/env python
#-encoding:utf-8-
from __future__ import with_statement
from optparse import OptionParser
import os
import sys
import ConfigParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

parser = OptionParser()
parser.add_option("-i","--init",action="store_false",dest="run_as_update",default=False,
    help="run the program as init,if this is the first time start the program,run the command with the parameter")
parser.add_option("-u","--update",action="store_true",dest="run_as_update",default=True,
    help="run the program as update,if this is not the first time you run the program")


def run_scrapy_spider(run_type):

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
        if run_type=="timing_run":
            to_run_spiders = config_parser.options("timing_run")
        elif run_type=="initial_run":
            to_run_spiders = config_parser.options("initial_run")
        else:
            print "error command type"
            sys.exit()
     
    process = CrawlerProcess(get_project_settings())
    
    for spider in to_run_spiders:
        process.crawl(spider)
    process.start()



if __name__ == "__main__":

    (cmd_options, cmd_args) = parser.parse_args()

    if cmd_options.run_as_update:
        RUN_TYPE="timing_run"
    else:
        RUN_TYPE = "initial_run"

    run_scrapy_spider(RUN_TYPE)

    
