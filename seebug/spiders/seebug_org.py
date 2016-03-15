#!-*-encoding:utf-8-*-
from scrapy.spiders import Spider
import scrapy
from seebug.itemLoaders import BugLoader
from seebug.items import BugItem

from scrapy.exceptions import CloseSpider
import datetime
import os 
from os.path import dirname

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
			'seebug.pipelines.SeebugPipeline': 300,			
			},
		 }
         
    max_page_num = 4000   
    
    current_page = 1
    
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
            bug_detail_request.meta['page'] = self.current_page
            yield bug_detail_request
        
        self.current_page += 1
        next_url = "https://www.seebug.org/vuldb/vulnerabilities?page={0}".format(self.current_page)
        
        yield scrapy.Request(next_url,callback = self.parse) 
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
        bug_item = BugLoader(item=BugItem(),response=response)
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
        return bug_item.load_item()
        
        
        
        
        