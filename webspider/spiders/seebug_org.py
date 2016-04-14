#!-*-encoding:utf-8-*-
import datetime
import os 
from os.path import dirname

from scrapy.spiders import Spider
import scrapy
from scrapy.exceptions import CloseSpider

from webspider.itemLoaders import SeeBugLoader
from webspider.items import SeeBugItem
from webspider.settings import TOP_DIR
#from webspider.util import config_jobdir


class SeebugSpider(Spider):
    """
    """
    
    name = "seebug"
    
    start_urls = [
        "https://www.seebug.org/vuldb/vulnerabilities"
    ]
    
    allowed_domains = ["www.seebug.org"]
    
    custom_settings={
		'ITEM_PIPELINES':
			{
			'webspider.pipelines.SeebugPipeline': 300,			
			},
        'JOBDIR':os.path.join(TOP_DIR,'seebug_spider_runtime'),
		 }
         
    max_page_num = 4000   
    
    #current_page = 1
    
    def parse(self,response):
        """
            /html/body/div[2]/div/div/div/div/table
            https://www.seebug.org/vuldb/vulnerabilities?page=2517
        """
        bug_pages = response.css("table.table.sebug-table.table-vul-list > tbody > tr")
        for one_page in bug_pages:
            
            one_page_url = one_page.xpath("./td[@class='vul-title-wrapper']/a/@href").extract()[0]
            link = response.urljoin(one_page_url)
            bug_detail_request = scrapy.Request(link,callback=self.parse_one)
            yield bug_detail_request
        
        #self.current_page += 1
        #next_url = "https://www.seebug.org/vuldb/vulnerabilities?page={0}".format(self.current_page)
        next_page_path = response.xpath("//ul[@class='pagination']/li[@class='active']/following-sibling::li[1]/a/@href").extract()
        current_page_num = response.xpath("//ul[@class='pagination']/li[@class='active']/a/text()").extract()[0]

        if next_page_path and int(current_page_num) < self.max_page_num:
            next_url = response.urljoin(next_page_path[0])
            yield scrapy.Request(next_url,callback = self.parse) 
        #else:
        #    raise CloseSpider("no more pages")
        #next_page_path = response.xpath("//ul[@class='pagination']/li[@class='active']/following-sibling::li[1]/a/@href").extract()
        #if next_page_path:
        #    next_url = response.urljoin(next_page_path[0])
        #    print next_url
            
    def parse_one(self,response):
        """
            section#j-vul-basic-info > div.row > div.col-md-6:nth-of-type(2)
            vul-basic-info
        """
        #print response.meta.get("page")
        #print response.xpath("//title/text()").extract()[0]
        bug_item = SeeBugLoader(item=SeeBugItem(),response=response)
        bug_item.add_css('title',"h1#j-vul-title::text")
        bug_item.add_css("ssvid","section#j-vul-basic-info > div.row > div.col-md-6:nth-of-type(1) > dl:nth-of-type(1) >dd >a::text")
        bug_item.add_css("discover_time","section#j-vul-basic-info > div.row > div.col-md-6:nth-of-type(1) > dl:nth-of-type(2) >dd::text")
        bug_item.add_css("commit_time","section#j-vul-basic-info > div.row > div.col-md-6:nth-of-type(1) > dl:nth-of-type(3) >dd::text")
        #danger_level = response.xpath("//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][1]/dl[4]/dd/div/@class").extract()
        bug_item.add_xpath("danger_level","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][1]/dl[4]/dd/div/@class")
        #print response.xpath("//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][1]/dl[4]/dd/div/@class").extract()[0]
        bug_item.add_xpath("bug_type","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][1]/dl[5]/dd/a/text()")
        
        bug_item.add_xpath("cveid","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][2]/dl[1]/dd/a/text()")
        bug_item.add_xpath("cnnydid","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][2]/dl[2]/dd/a/text()")
        bug_item.add_xpath("cnvdid","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][2]/dl[3]/dd/a/text()")
        bug_item.add_xpath("author","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][2]/dl[4]/dd/a/text()")
        bug_item.add_xpath("commitor","//section[@id='j-vul-basic-info']/div[@class='row']/div[@class='col-md-6'][2]/dl[5]/dd/a/text()")
        
        bug_item.add_xpath("zoomeye_dork","//section[@id='j-vul-basic-info']/dl[1]/dd/a/text()")
        bug_item.add_xpath("influence_component","//section[@id='j-vul-basic-info']/dl[2]/dd/a/text()")
        
        bug_item.add_xpath("bug_abstract","//div[@id='j-md-summary']/text()")
        bug_item.add_value("url",response.url)
        return bug_item.load_item()
        
        
        
class SeebugUpdator(SeebugSpider):
    """
        跟新模块
    """     
    start_urls = [
        "https://www.seebug.org/vuldb/vulnerabilities"
    ] 

    name = "seebug_updator"

    max_page_num = 3

    custom_settings={
		'ITEM_PIPELINES':
			{
			'webspider.pipelines.SeebugPipeline': 300,			
			},
		 }       
        